"""
Salon Pro Views - Complete System
"""
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decimal import Decimal
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

import requests
from django.views.decorators.csrf import csrf_exempt


from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
import os

from .models import (
    Branch, User, Service, Product, Bank, Customer,
    Invoice, InvoiceItem, Booking, Expense, StockMovement, DailyQueueNumber,
    PurchaseInvoice, PurchaseInvoiceItem,
    ConsumptionInvoice, ConsumptionInvoiceItem,
    ExpenseType, ExpenseVoucher,
    SalonSettings, Employee, ActivityLog, AccountTransfer,
)
from .backup_utils import create_backup_sql, restore_backup_sql, latest_backup_info
from .audit_utils import (
    log_activity, ACTION_CREATE, ACTION_UPDATE, ACTION_DELETE, ACTION_VOID,
    T_INVOICE, T_BOOKING, T_PRODUCT, T_PURCHASE, T_CONSUMPTION,
    T_EXPENSE_TYPE, T_EXPENSE_VOUCHER, T_SERVICE, T_CUSTOMER, T_EMPLOYEE,
    T_USER, T_STOCK, T_SETTINGS, T_BACKUP, T_ACCOUNT_TRANSFER,
)
from .permissions import (
    PERMISSION_GROUPS, apply_user_permissions, has_perm, permissions_dict,
    user_permissions_payload,
)
from .statement_utils import (
    build_bank_statement, build_cash_statement, build_transfer_statement,
    get_active_banks, get_statement_branch,
)
from .forms import (
    LoginForm, UserForm, ServiceForm, ProductForm,
    BankForm, CustomerForm, BookingForm, ExpenseForm, StockMovementForm
)


# =============================================================================
# HELPERS
# =============================================================================

def get_user_branch(request):
    """Get branch for current user"""
    if request.user.is_superuser:
        return None
    return request.user.branch


def get_branch_queryset(request, model, order_by='-created_at'):
    """Get queryset filtered by user branch"""
    branch = get_user_branch(request)
    
    # لو الموديل المطلوب هو الخدمة، رجع كل الخدمات لأنها غير مقسمة بفروع في قاعدة البيانات
    if model.__name__ == 'Service':
        return model.objects.all().order_by(order_by)

    if model.__name__ == 'Invoice':
        base = model.objects.filter(is_voided=False)
        if branch:
            return base.filter(branch=branch).order_by(order_by)
        return base.order_by(order_by)
        
    if branch:
        # لباقي الموديلات اللي فيها فروع زي الفواتير والمبيعات
        try:
            return model.objects.filter(branch=branch).order_by(order_by)
        except Exception:
            return model.objects.all().order_by(order_by)
            
    return model.objects.all().order_by(order_by)


def _resolve_employee(branch, data):
    """Resolve employee from code or id for the given branch."""
    if not branch:
        return None
    employee_code = str(data.get('employee_code', '')).strip()
    if employee_code:
        return Employee.objects.filter(
            branch=branch, serial_number=employee_code, is_active=True,
        ).first()
    employee_id = data.get('employee')
    if employee_id:
        return Employee.objects.filter(
            branch=branch, id=employee_id, is_active=True,
        ).first()
    return None


def _employee_performance(invoices):
    return invoices.filter(employee__isnull=False).values(
        'employee__name',
    ).annotate(
        total_sales=Sum('final_total'),
        invoice_count=Count('id'),
    ).order_by('-total_sales')


# =============================================================================
# AUTH
# =============================================================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"👋 أهلاً {user.get_full_name() or user.username}!")
            return redirect('dashboard')
        messages.error(request, "❌ اسم المستخدم أو كلمة المرور غير صحيحة")
    else:
        form = LoginForm()

    return render(request, 'salon/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "✅ تم تسجيل الخروج بنجاح")
    return redirect('login')


# =============================================================================
# DASHBOARD
# =============================================================================

@login_required
def dashboard(request):
    user = request.user
    branch = get_user_branch(request)
    today = timezone.now().date()

    # Stats
    if branch:
        invoices_today = Invoice.objects.filter(branch=branch, created_at__date=today, is_voided=False)
        expenses_today = ExpenseVoucher.objects.filter(branch=branch, date=today)
        waiting = Booking.objects.filter(branch=branch, status='waiting').count()
        low_stock = Product.objects.filter(branch=branch, stock__lte=F('min_stock')).count()
        # <-- هنا المشكلة: لازم يكون queue مش bookings
        queue = Booking.objects.filter(branch=branch, status__in=['waiting', 'in_progress']).order_by('queue_number')[:10]
    else:
        invoices_today = Invoice.objects.filter(created_at__date=today, is_voided=False)
        expenses_today = ExpenseVoucher.objects.filter(date=today)
        waiting = Booking.objects.filter(status='waiting').count()
        low_stock = Product.objects.filter(stock__lte=F('min_stock')).count()
        queue = Booking.objects.filter(status__in=['waiting', 'in_progress']).order_by('queue_number')[:10]

    revenue = invoices_today.aggregate(total=Sum('final_total'))['total'] or 0
    exp_out = expenses_today.filter(voucher_type='out').aggregate(total=Sum('amount'))['total'] or 0
    exp_ret = expenses_today.filter(voucher_type='return').aggregate(total=Sum('amount'))['total'] or 0
    expenses = exp_out - exp_ret

    # Recent invoices
    recent = get_branch_queryset(request, Invoice)[:10]

    context = {
        'revenue': revenue,
        'expenses': expenses,
        'waiting': waiting,
        'low_stock': low_stock,
        'queue': queue,  # <-- لازم يكون 'queue'
        'recent_invoices': recent,
        'today': today,
    }
    return render(request, 'salon/dashboard.html', context)


# =============================================================================
# send_whatsapp_invoice
# =============================================================================

@login_required
@csrf_protect
def send_whatsapp_invoice(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone = data.get('phone', '').replace(" ", "")
            invoice_number = data.get('invoice_number', '')
            invoice_id = data.get('invoice_id', '')

            if not phone:
                return JsonResponse({"success": False, "error": "ادخل رقم واتساب العميل"})

            api_key = getattr(settings, "WHATSAPP_API_KEY", None)
            api_url = getattr(settings, "WHATSAPP_API_URL", None)
            if not api_key or not api_url:
                return JsonResponse({
                    "success": False,
                    "error": "إعدادات واتساب غير مكتملة في السيرفر",
                })
            
            if phone.startswith('0'):
                phone = '2' + phone
                
            message = f"*{settings.PROJECT_NAME}*\n\nعزيزي العميل، تم إصدار فاتورتك بنجاح.\n📄 فاتورة رقم: #{invoice_number}\n🔗 لمشاهدة الفاتورة: {request.build_absolute_uri(f'/invoice/{invoice_id}/receipt/')}\n\nشكراً لزيارتك! 🙏"

            # 🎯 الـتـعـديـل الـقـاطـع: أسماء الـ Keys كما هي في قاعدة بيانات السيرفر بالظبط
            payload = {
                "to_number": phone,   # اتغيرت من to لـ to_number
                "body": message,
                "project_id": 29      # 👈 ضيف الـ id بتاع الحساب اللي أخدت الكي بتاعه (زي ما ظاهر في الـ pgAdmin)
            }

            headers = {
                "Authorization": f"Token {api_key}",
                "Content-Type": "application/json",
                "Host": "laperla.e-jewelrybysoftwarehouse.com", 
                "Origin": "https://laperla.e-jewelrybysoftwarehouse.com"
            }
            
            url = f"{api_url}/accounts/messages/"
            
            # الإرسال كـ JSON ليفهمه السيرفر تماماً
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code in [200, 201]:
                return JsonResponse({"success": True})
            else:
                return JsonResponse({
                    "success": False, 
                    "error": f"السيرفر رد بكود {response.status_code}: {response.text}"
                })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
            
    return JsonResponse({"success": False, "error": "Method not allowed"})


# =============================================================================
# POS
# =============================================================================

@login_required
def pos(request):
    if not request.user.can_pos:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    branch = get_user_branch(request)
    if not branch and not request.user.is_superuser:
        messages.error(request, "🏪 لم يتم تعيين فرع لهذا المستخدم")
        return redirect('dashboard')

    if branch:
        services = Service.objects.filter(is_active=True)
        banks = get_active_banks()
        employees = Employee.objects.filter(branch=branch, is_active=True).order_by('serial_number')
    else:
        services = Service.objects.filter(is_active=True)
        banks = get_active_banks()
        employees = Employee.objects.filter(is_active=True).order_by('branch', 'serial_number')

    if request.method == 'POST':
        data = json.loads(request.body)
        items = data.get('items', [])
        invoice_id = data.get('invoice_id')
        booking_id = data.get('booking_id')

        if not items:
            return JsonResponse({'success': False, 'error': 'السلة فارغة!'})

        invoice_branch = branch or Branch.objects.first()
        if invoice_id:
            try:
                invoice_branch = Invoice.objects.get(
                    id=invoice_id, is_voided=False,
                ).branch
            except Invoice.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'الفاتورة غير موجودة'})

        if not invoice_branch:
            return JsonResponse({'success': False, 'error': 'لا يوجد فرع نشط'})

        if not _resolve_employee(invoice_branch, data):
            return JsonResponse({
                'success': False,
                'error': 'الموظف مطلوب — اختره من القائمة أو أدخل كوده',
            })

        try:
            with transaction.atomic():
                if invoice_id:
                    invoice = Invoice.objects.select_for_update().get(
                        id=invoice_id, is_voided=False,
                    )
                    if timezone.localtime(invoice.created_at).date() != timezone.localdate():
                        return JsonResponse({
                            'success': False,
                            'error': 'التعديل مسموح على فواتير اليوم فقط',
                        })
                    
                    if invoice.customer:
                        invoice.customer.total_spent -= invoice.final_total
                        invoice.customer.save()
                    
                    invoice.items.all().delete()
                else:
                    invoice = Invoice()
                    invoice.branch = branch or Branch.objects.first()
                    invoice.created_by = request.user

                customer_name = data.get('customer_name', '').strip()
                customer_phone = data.get('customer_phone', '').strip()
                if customer_name:
                    customer, _ = Customer.objects.get_or_create(
                        branch=invoice.branch, 
                        phone=customer_phone,
                        defaults={'name': customer_name}
                    )
                    invoice.customer = customer
                else:
                    invoice.customer = None

                invoice.employee = _resolve_employee(invoice.branch, data)
                invoice.barber = None

                invoice.payment_method = data.get('payment_method', 'cash')
                bank_id = data.get('bank')
                if invoice.payment_method == 'bank' and bank_id:
                    invoice.bank = Bank.objects.get(id=bank_id)
                else:
                    invoice.bank = None

                invoice.discount = Decimal(data.get('discount', 0) or 0)
                invoice.notes = data.get('notes', '')

                if booking_id:
                    booking_obj = Booking.objects.filter(
                        id=booking_id, branch=invoice.branch, is_vip=True,
                    ).first()
                    if booking_obj:
                        invoice.booking = booking_obj
                
                invoice.save()

                subtotal = 0
                for item in items:
                    service = Service.objects.get(id=item['id'])
                    item_total = Decimal(item['qty']) * Decimal(item['price'])
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        service=service,
                        quantity=item['qty'],
                        price=Decimal(item['price']),
                        total=item_total
                    )
                    subtotal += item_total

                invoice.subtotal = subtotal
                invoice.save()

                if invoice.customer:
                    if not invoice_id:
                        invoice.customer.visits_count += 1
                    invoice.customer.total_spent += invoice.final_total
                    invoice.customer.save()

                if invoice.booking_id:
                    b = invoice.booking
                    b.status = 'completed'
                    b.completed_at = timezone.now()
                    if not b.started_at:
                        b.started_at = timezone.now()
                    b.save(update_fields=['status', 'completed_at', 'started_at'])

            log_activity(
                request,
                ACTION_UPDATE if invoice_id else ACTION_CREATE,
                T_INVOICE,
                f'#{invoice.display_number()} — {invoice.final_total} ج.م',
                invoice.id,
                invoice.branch,
            )

            return JsonResponse({
                'success': True,
                'message': '✅ تم الحفظ بنجاح!',
                'invoice_id': invoice.id,
                'invoice_number': str(invoice.display_number()),
                'serial_number': invoice.serial_number,
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    context = {
        'services': services,
        'banks': banks,
        'employees': employees,
    }
    return render(request, 'salon/pos.html', context)


@login_required
def get_invoice_json(request, invoice_id):
    """جلب فاتورة بالمعرف."""
    try:
        branch = get_user_branch(request)
        qs = Invoice.objects.filter(id=invoice_id, is_voided=False)
        if branch:
            qs = qs.filter(branch=branch)
        invoice = qs.get()
        return JsonResponse(_invoice_payload(invoice))
    except Invoice.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'الفاتورة غير موجودة'})


@login_required
def pos_lookup_invoice(request):
    """جلب فاتورة بالمسلسل (1، 2، 3...)."""
    q = request.GET.get('serial', '').strip()
    if not q.isdigit():
        return JsonResponse({'success': False, 'error': 'أدخل رقم المسلسل'})
    branch = get_user_branch(request)
    qs = Invoice.objects.filter(is_voided=False, serial_number=int(q))
    if branch:
        qs = qs.filter(branch=branch)
    invoice = qs.first()
    if not invoice:
        return JsonResponse({'success': False, 'error': 'فاتورة غير موجودة'})
    return JsonResponse(_invoice_payload(invoice))


@login_required
def pos_lookup_booking(request):
    """جلب حجز VIP برقم الدور."""
    q = request.GET.get('queue', '').strip()
    if not q.isdigit():
        return JsonResponse({'success': False, 'error': 'أدخل رقم الحجز'})
    branch = get_user_branch(request)
    today = timezone.localdate()
    qs = Booking.objects.filter(
        is_vip=True, queue_number=int(q), created_at__date=today,
    )
    if branch:
        qs = qs.filter(branch=branch)
    booking = qs.prefetch_related('services').first()
    if not booking:
        return JsonResponse({'success': False, 'error': 'حجز VIP غير موجود'})
    if booking.status == 'completed':
        return JsonResponse({'success': False, 'error': 'هذا الحجز تم تنفيذه'})
    if booking.status == 'cancelled':
        return JsonResponse({'success': False, 'error': 'هذا الحجز ملغي'})
    return JsonResponse(_booking_payload(booking))


def _booking_payload(booking):
    items = [{
        'id': s.id,
        'name': s.name,
        'price': str(s.price),
        'qty': 1,
    } for s in booking.services.all()]
    return {
        'success': True,
        'booking': {
            'id': booking.id,
            'queue_number': booking.queue_number,
            'customer_name': booking.customer_name,
            'customer_phone': booking.customer_phone,
            'barber_id': booking.barber.id if booking.barber else '',
            'employee_code': booking.employee.serial_number if booking.employee else '',
            'employee_name': booking.employee.name if booking.employee else '',
            'notes': booking.notes,
            'items': items,
            'status': booking.status,
        },
    }


def _invoice_payload(invoice):
    items_data = [{
        'id': item.service.id if item.service else None,
        'name': item.service.name if item.service else (
            item.product.name if item.product else '—'
        ),
        'price': str(item.price),
        'qty': item.quantity,
    } for item in invoice.items.all()]
    return {
        'success': True,
        'invoice': {
            'id': invoice.id,
            'serial_number': invoice.serial_number,
            'invoice_number': str(invoice.display_number()),
            'customer_name': invoice.customer.name if invoice.customer else '',
            'customer_phone': invoice.customer.phone if invoice.customer else '',
            'barber_id': invoice.barber.id if invoice.barber else '',
            'employee_code': invoice.employee.serial_number if invoice.employee else '',
            'employee_name': invoice.employee.name if invoice.employee else '',
            'payment_method': invoice.payment_method,
            'bank_id': invoice.bank.id if invoice.bank else '',
            'discount': str(invoice.discount),
            'items': items_data,
            'can_edit': invoice.can_edit_today(),
            'created_at': invoice.created_at.strftime('%Y-%m-%d %H:%M'),
        },
    }


@login_required
@require_POST
def pos_void_invoice(request, pk):
    """إلغاء فاتورة — خلال اليوم فقط."""
    if not require_access_json(request, 'can_delete_pos'):
        return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية الحذف'})
    branch = get_user_branch(request)
    qs = Invoice.objects.filter(pk=pk, is_voided=False)
    if branch:
        qs = qs.filter(branch=branch)
    invoice = get_object_or_404(qs)
    if not invoice.can_edit_today():
        return JsonResponse({'success': False, 'error': 'الحذف مسموح خلال اليوم فقط'})
    if invoice.customer:
        invoice.customer.total_spent -= invoice.final_total
        if invoice.customer.visits_count > 0:
            invoice.customer.visits_count -= 1
        invoice.customer.save()
    invoice.is_voided = True
    invoice.save(update_fields=['is_voided'])
    log_activity(
        request, ACTION_VOID, T_INVOICE,
        f'#{invoice.display_number()}', invoice.id, invoice.branch,
    )
    return JsonResponse({'success': True, 'message': f'تم إلغاء الفاتورة #{invoice.display_number()}'})
# =============================================================================
# INVOICE PRINT
# =============================================================================

@login_required
def invoice_print(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'salon/invoice_print.html', {'invoice': invoice})


# =============================================================================
# BOOKINGS
# =============================================================================

@login_required
def booking_list(request):
    if not (
        has_perm(request.user, 'can_bookings')
        or has_perm(request.user, 'can_booking_vip')
        or has_perm(request.user, 'can_booking_queue')
    ):
        return redirect('dashboard')
    bookings = get_branch_queryset(request, Booking, 'queue_number')
    return render(request, 'salon/booking_list.html', {'bookings': bookings})


@login_required
def booking_add(request):
    if not require_access(request, 'can_booking_vip'):
        return redirect('dashboard')
    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    if not branch:
        messages.error(request, "لا يوجد فرع نشط")
        return redirect('dashboard')

    services = Service.objects.filter(is_active=True)
    employees = Employee.objects.filter(branch=branch, is_active=True).order_by('serial_number')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])
            customer_name = data.get('customer_name', '').strip()
            customer_phone = data.get('customer_phone', '').strip()

            if not customer_name or not customer_phone:
                return JsonResponse({
                    'success': False,
                    'error': 'الاسم ورقم الهاتف مطلوبان',
                })
            if not items:
                return JsonResponse({
                    'success': False,
                    'error': 'اختر خدمة واحدة على الأقل',
                })
            if not _resolve_employee(branch, data):
                return JsonResponse({
                    'success': False,
                    'error': 'الموظف مطلوب — اختره من القائمة أو أدخل كوده',
                })

            today = timezone.localdate()
            last = Booking.objects.filter(
                branch=branch, created_at__date=today,
            ).order_by('-queue_number').first()
            queue_number = (last.queue_number + 1) if last else 1

            booking = Booking(
                branch=branch,
                customer_name=customer_name,
                customer_phone=customer_phone,
                queue_number=queue_number,
                is_vip=True,
                status='waiting',
                notes=data.get('notes', ''),
            )
            booking.employee = _resolve_employee(branch, data)
            booking.barber = None
            booking.save()

            service_ids = [item['id'] for item in items]
            booking.services.set(Service.objects.filter(id__in=service_ids))

            log_activity(
                request, ACTION_CREATE, T_BOOKING,
                f'VIP رقم {queue_number} — {customer_name}',
                booking.id, branch,
            )

            return JsonResponse({
                'success': True,
                'message': f'تم حجز VIP رقم {queue_number}',
                'queue_number': queue_number,
                'booking_id': booking.id,
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'salon/booking_form.html', {
        'services': services,
        'employees': employees,
    })

@login_required
@require_POST
def booking_status(request, pk):
    if not require_access(request, 'can_bookings'):
        return redirect('dashboard')
    booking = get_object_or_404(Booking, pk=pk)
    status = request.POST.get('status')

    if status == 'in_progress':
        booking.status = 'in_progress'
        booking.started_at = timezone.now()
    elif status == 'completed':
        booking.status = 'completed'
        booking.completed_at = timezone.now()
    elif status == 'cancelled':
        booking.status = 'cancelled'

    booking.save()
    status_labels = {
        'in_progress': 'بدء التنفيذ',
        'completed': 'إكمال',
        'cancelled': 'إلغاء',
    }
    if status in status_labels:
        log_activity(
            request, ACTION_UPDATE, T_BOOKING,
            f'{booking.customer_name} — {status_labels[status]}',
            booking.id, booking.branch,
        )
    return JsonResponse({'success': True})



@login_required
@require_POST
def print_queue_number(request):
    """Generate and print a new queue number without booking data"""
    if not require_access_json(request, 'can_booking_queue'):
        return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية'})
    branch = get_user_branch(request)
    if not branch:
        branch = Branch.objects.filter(is_active=True).first()
    
    if not branch:
        return JsonResponse({'success': False, 'error': 'لا يوجد فرع'})
    
    today = timezone.now().date()
    
    # Get or create daily counter
    daily_counter, created = DailyQueueNumber.objects.get_or_create(
        branch=branch,
        date=today,
        defaults={'last_number': 0}
    )
    
    # Get next number
    next_number = daily_counter.get_next_number()

    print_url = (
        f'/queue/receipt/?number={next_number}'
        f'&branch={branch.name}'
        f'&date={today.strftime("%Y-%m-%d")}'
        f'&time={timezone.now().strftime("%H:%M")}'
    )

    return JsonResponse({
        'success': True,
        'number': next_number,
        'branch': branch.name,
        'date': today.strftime('%Y-%m-%d'),
        'time': timezone.now().strftime('%H:%M'),
        'print_url': print_url,
    })

# =============================================================================
# INVENTORY
# =============================================================================

def _apply_purchase_lines(purchase, items, branch, user):
    for row in items:
        product = Product.objects.select_for_update().get(
            id=row['product_id'], branch=branch,
        )
        qty = int(row['quantity'])
        cost = Decimal(str(row['cost']))
        price = Decimal(str(row['price']))
        if qty <= 0:
            raise ValueError('الكمية يجب أن تكون أكبر من صفر')

        PurchaseInvoiceItem.objects.create(
            purchase=purchase,
            product=product,
            quantity=qty,
            cost=cost,
            price=price,
        )
        product.cost = cost
        product.price = price
        product.save(update_fields=['cost', 'price'])

        StockMovement.objects.create(
            branch=branch,
            product=product,
            movement_type='in',
            quantity=qty,
            cost=cost,
            notes=f'مشتريات #{purchase.serial_number}',
            created_by=user,
            reference_invoice=purchase,
        )


def _apply_consumption_lines(consumption, items, branch, user):
    for row in items:
        product = Product.objects.select_for_update().get(
            id=row['product_id'], branch=branch,
        )
        qty = int(row['quantity'])
        if qty <= 0:
            raise ValueError('الكمية يجب أن تكون أكبر من صفر')
        if product.stock < qty:
            raise ValueError(f'المخزون غير كافٍ للصنف {product.name} (متاح: {product.stock})')

        ConsumptionInvoiceItem.objects.create(
            consumption=consumption,
            product=product,
            quantity=qty,
            unit_cost=product.cost,
        )
        StockMovement.objects.create(
            branch=branch,
            product=product,
            movement_type='out',
            quantity=qty,
            cost=product.cost,
            notes=f'استهلاك #{consumption.serial_number}',
            created_by=user,
            reference_consumption=consumption,
        )


def _consumption_payload(consumption):
    items = [{
        'product_id': i.product_id,
        'name': i.product.name,
        'code': i.product.code,
        'quantity': i.quantity,
        'unit_cost': str(i.unit_cost),
    } for i in consumption.items.select_related('product')]
    return {
        'success': True,
        'consumption': {
            'id': consumption.id,
            'serial_number': consumption.serial_number,
            'items': items,
        },
    }


def _inventory_report_context(branch):
    purchase_items = PurchaseInvoiceItem.objects.select_related(
        'product', 'purchase',
    ).order_by('-purchase__created_at')
    consumption_items = ConsumptionInvoiceItem.objects.select_related(
        'product', 'consumption',
    ).order_by('-consumption__created_at')
    if branch:
        purchase_items = purchase_items.filter(purchase__branch=branch)
        consumption_items = consumption_items.filter(consumption__branch=branch)

    incoming = []
    grand_in_cost = Decimal('0')
    grand_in_sale = Decimal('0')
    for item in purchase_items[:500]:
        grand_in_cost += item.line_cost
        grand_in_sale += item.line_price
        incoming.append({
            'serial': item.purchase.serial_number,
            'date': item.purchase.created_at,
            'code': item.product.code,
            'name': item.product.name,
            'qty': item.quantity,
            'cost': item.cost,
            'price': item.price,
            'line_cost': item.line_cost,
            'line_sale': item.line_price,
        })

    outgoing = []
    grand_out_qty = 0
    grand_out_cost = Decimal('0')
    for item in consumption_items[:500]:
        grand_out_qty += item.quantity
        grand_out_cost += item.line_cost
        outgoing.append({
            'serial': item.consumption.serial_number,
            'date': item.consumption.created_at,
            'code': item.product.code,
            'name': item.product.name,
            'qty': item.quantity,
            'unit_cost': item.unit_cost,
            'line_cost': item.line_cost,
        })

    net_qty = sum(i['qty'] for i in incoming) - grand_out_qty
    net_cost = grand_in_cost - grand_out_cost
    net_sale = grand_in_sale - grand_out_cost

    return {
        'incoming': incoming,
        'outgoing': outgoing,
        'grand_in_cost': grand_in_cost,
        'grand_in_sale': grand_in_sale,
        'grand_out_qty': grand_out_qty,
        'grand_out_cost': grand_out_cost,
        'net_qty': net_qty,
        'net_cost': net_cost,
        'net_sale': net_sale,
    }


def _render_inventory_pdf(request, template, context, filename):
    html_string = render_to_string(template, context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    css_path = os.path.join(settings.BASE_DIR, 'salon', 'static', 'css', 'pdf_rtl.css')
    if os.path.exists(css_path):
        pdf = html.write_pdf(stylesheets=[CSS(css_path)])
    else:
        pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response


def _purchase_payload(purchase):
    items = [{
        'product_id': i.product_id,
        'name': i.product.name,
        'code': i.product.code,
        'cost': str(i.cost),
        'price': str(i.price),
        'quantity': i.quantity,
    } for i in purchase.items.select_related('product')]
    return {
        'success': True,
        'purchase': {
            'id': purchase.id,
            'serial_number': purchase.serial_number,
            'items': items,
        },
    }


@login_required
def inventory(request):
    if not require_access(request, 'can_inventory'):
        return redirect('dashboard')

    products = get_branch_queryset(request, Product, 'name')
    low_stock = products.filter(stock__lte=F('min_stock'))
    out_of_stock = products.filter(stock__lte=0)

    return render(request, 'salon/inventory.html', {
        'products': products,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
    })


@login_required
def inventory_item_add(request):
    """تكويد صنف — كود تلقائي + استرجاع بالكود."""
    if not require_access(request, 'can_inv_items'):
        return redirect('dashboard')

    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    if not branch:
        messages.error(request, "لا يوجد فرع نشط")
        return redirect('inventory')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action', 'save')
            product_id = data.get('product_id')
            code = str(data.get('code', '')).strip()
            name = data.get('name', '').strip()

            if action == 'delete':
                if not require_access_json(request, 'can_delete_inventory'):
                    return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية الحذف'})
                if not product_id:
                    return JsonResponse({'success': False, 'error': 'اختر صنفاً أولاً'})
                product = Product.objects.get(id=product_id, branch=branch)
                ok, msg = product.can_delete_catalog()
                if not ok:
                    return JsonResponse({'success': False, 'error': msg})
                label = f'{product.code} — {product.name}'
                product.delete()
                log_activity(request, ACTION_DELETE, T_PRODUCT, label, product_id, branch)
                return JsonResponse({
                    'success': True,
                    'message': 'تم حذف الصنف',
                    'next_code': Product.next_code(branch),
                })

            if not name:
                return JsonResponse({'success': False, 'error': 'اسم الصنف مطلوب'})

            if product_id:
                product = Product.objects.get(id=product_id, branch=branch)
                product.name = name
                product.save(update_fields=['name'])
                log_activity(
                    request, ACTION_UPDATE, T_PRODUCT,
                    f'{product.code} — {name}', product.id, branch,
                )
                return JsonResponse({'success': True, 'message': 'تم تحديث الصنف'})

            if not code:
                code = Product.next_code(branch)
            elif Product.objects.filter(branch=branch, code=code).exists():
                return JsonResponse({'success': False, 'error': f'كود {code} موجود — اضغط Enter لتحميله'})

            Product.objects.create(
                branch=branch, code=code, name=name,
                price=0, cost=0, stock=0,
            )
            log_activity(request, ACTION_CREATE, T_PRODUCT, f'{code} — {name}', None, branch)
            return JsonResponse({
                'success': True,
                'message': f'تم تكويد الصنف {name}',
                'next_code': Product.next_code(branch),
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'salon/inventory_item_form.html', {
        'next_code': Product.next_code(branch),
    })


@login_required
def inventory_item_lookup(request):
    code = request.GET.get('code', '').strip()
    if not code:
        return JsonResponse({'success': False, 'error': 'أدخل كود الصنف'})
    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    product = Product.objects.filter(branch=branch, code=code).first()
    if not product:
        return JsonResponse({'success': False, 'error': 'صنف غير موجود'})
    can_del, del_msg = product.can_delete_catalog()
    if not has_perm(request.user, 'can_delete_inventory'):
        can_del, del_msg = False, 'ليس لديك صلاحية الحذف'
    return JsonResponse({
        'success': True,
        'product': {
            'id': product.id,
            'code': product.code,
            'name': product.name,
            'stock': product.stock,
            'can_delete': can_del,
            'delete_message': del_msg,
        },
    })


@login_required
def inventory_purchase_add(request):
    """فاتورة مشتريات مخزن — عدة أصناف."""
    if not require_access(request, 'can_inv_purchase'):
        return redirect('dashboard')

    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    if not branch:
        messages.error(request, "لا يوجد فرع نشط")
        return redirect('inventory')

    products = Product.objects.filter(branch=branch, is_active=True).order_by('name')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])
            purchase_id = data.get('purchase_id')
            if not items:
                return JsonResponse({'success': False, 'error': 'أضف صنفاً واحداً على الأقل'})

            with transaction.atomic():
                if purchase_id:
                    purchase = PurchaseInvoice.objects.select_for_update().get(
                        id=purchase_id, branch=branch,
                    )
                    purchase.reverse_stock()
                else:
                    purchase = PurchaseInvoice(
                        branch=branch,
                        created_by=request.user,
                        notes=data.get('notes', ''),
                    )
                    purchase.save()

                _apply_purchase_lines(purchase, items, branch, request.user)

            log_activity(
                request,
                ACTION_UPDATE if purchase_id else ACTION_CREATE,
                T_PURCHASE,
                f'#{purchase.serial_number}',
                purchase.id, branch,
            )

            return JsonResponse({
                'success': True,
                'serial_number': purchase.serial_number,
                'purchase_id': purchase.id,
                'message': f'تم حفظ فاتورة المشتريات #{purchase.serial_number}',
                'next_serial': PurchaseInvoice.next_serial(branch),
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'salon/inventory_purchase.html', {
        'products': products,
        'next_serial': PurchaseInvoice.next_serial(branch),
    })


@login_required
def inventory_purchase_lookup(request):
    q = request.GET.get('serial', '').strip()
    if not q.isdigit():
        return JsonResponse({'success': False, 'error': 'أدخل رقم المسلسل'})
    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    qs = PurchaseInvoice.objects.prefetch_related('items__product')
    if branch:
        qs = qs.filter(branch=branch)
    purchase = qs.filter(serial_number=int(q)).first()
    if not purchase:
        return JsonResponse({'success': False, 'error': 'فاتورة غير موجودة'})
    return JsonResponse(_purchase_payload(purchase))


@login_required
@require_POST
def inventory_purchase_delete(request, pk):
    if not require_access_json(request, 'can_delete_inventory'):
        return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية الحذف'})
    branch = get_user_branch(request)
    qs = PurchaseInvoice.objects.filter(pk=pk)
    if branch:
        qs = qs.filter(branch=branch)
    purchase = get_object_or_404(qs)
    try:
        serial = purchase.serial_number
        with transaction.atomic():
            purchase.reverse_stock()
            purchase.delete()
        log_activity(
            request, ACTION_DELETE, T_PURCHASE,
            f'#{serial}', pk, branch or purchase.branch,
        )
        return JsonResponse({
            'success': True,
            'message': 'تم حذف فاتورة المشتريات',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def inventory_consumption_add(request):
    """أصناف مستهلكة — تقليل المخزون."""
    if not require_access(request, 'can_inv_consumption'):
        return redirect('dashboard')

    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    if not branch:
        messages.error(request, "لا يوجد فرع نشط")
        return redirect('inventory')

    products = Product.objects.filter(branch=branch, is_active=True, stock__gt=0).order_by('name')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])
            consumption_id = data.get('consumption_id')
            if not items:
                return JsonResponse({'success': False, 'error': 'أضف صنفاً واحداً على الأقل'})

            with transaction.atomic():
                if consumption_id:
                    consumption = ConsumptionInvoice.objects.select_for_update().get(
                        id=consumption_id, branch=branch,
                    )
                    consumption.reverse_stock()
                else:
                    consumption = ConsumptionInvoice(
                        branch=branch,
                        created_by=request.user,
                        notes=data.get('notes', ''),
                    )
                    consumption.save()

                _apply_consumption_lines(consumption, items, branch, request.user)

            log_activity(
                request,
                ACTION_UPDATE if consumption_id else ACTION_CREATE,
                T_CONSUMPTION,
                f'#{consumption.serial_number}',
                consumption.id, branch,
            )

            return JsonResponse({
                'success': True,
                'serial_number': consumption.serial_number,
                'consumption_id': consumption.id,
                'message': f'تم حفظ حركة الاستهلاك #{consumption.serial_number}',
                'next_serial': ConsumptionInvoice.next_serial(branch),
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'salon/inventory_consumption.html', {
        'products': products,
        'next_serial': ConsumptionInvoice.next_serial(branch),
    })


@login_required
def inventory_consumption_lookup(request):
    q = request.GET.get('serial', '').strip()
    if not q.isdigit():
        return JsonResponse({'success': False, 'error': 'أدخل رقم المسلسل'})
    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    qs = ConsumptionInvoice.objects.prefetch_related('items__product')
    if branch:
        qs = qs.filter(branch=branch)
    consumption = qs.filter(serial_number=int(q)).first()
    if not consumption:
        return JsonResponse({'success': False, 'error': 'حركة غير موجودة'})
    return JsonResponse(_consumption_payload(consumption))


@login_required
@require_POST
def inventory_consumption_delete(request, pk):
    if not require_access_json(request, 'can_delete_inventory'):
        return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية الحذف'})
    branch = get_user_branch(request)
    qs = ConsumptionInvoice.objects.filter(pk=pk)
    if branch:
        qs = qs.filter(branch=branch)
    consumption = get_object_or_404(qs)
    try:
        serial = consumption.serial_number
        with transaction.atomic():
            consumption.reverse_stock()
            consumption.delete()
        log_activity(
            request, ACTION_DELETE, T_CONSUMPTION,
            f'#{serial}', pk, branch or consumption.branch,
        )
        return JsonResponse({'success': True, 'message': 'تم حذف حركة الاستهلاك'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def inventory_report(request):
    """تقرير المشتريات والاستهلاك."""
    if not require_access(request, 'can_inv_report'):
        return redirect('dashboard')

    branch = get_user_branch(request)
    ctx = _inventory_report_context(branch)
    ctx['branch'] = branch
    return render(request, 'salon/inventory_report.html', ctx)


@login_required
def inventory_report_pdf(request):
    if not require_access(request, 'can_inv_report'):
        return redirect('dashboard')
    branch = get_user_branch(request)
    ctx = _inventory_report_context(branch)
    ctx.update({'branch': branch, 'now': timezone.now(), 'title': 'تقرير المشتريات والاستهلاك'})
    return _render_inventory_pdf(
        request, 'salon/inventory_report_pdf.html', ctx,
        f'inventory_report_{timezone.now().strftime("%Y%m%d")}.pdf',
    )


@login_required
def inventory_purchase_detail(request, pk):
    if not require_access(request, 'can_inv_purchase'):
        return redirect('dashboard')
    branch = get_user_branch(request)
    qs = PurchaseInvoice.objects.prefetch_related('items__product')
    if branch:
        qs = qs.filter(branch=branch)
    purchase = get_object_or_404(qs, pk=pk)
    return render(request, 'salon/inventory_purchase_detail.html', {
        'purchase': purchase,
        'total_cost': purchase.total_cost,
        'total_price': purchase.total_price,
    })


@login_required
def inventory_totals(request):
    """صافي إجماليات المخزون."""
    if not require_access(request, 'can_inv_totals'):
        return redirect('dashboard')

    branch = get_user_branch(request)
    products = Product.objects.filter(is_active=True)
    if branch:
        products = products.filter(branch=branch)

    rows = []
    grand_cost = Decimal('0')
    grand_sale = Decimal('0')

    for p in products.order_by('code', 'name'):
        agg = PurchaseInvoiceItem.objects.filter(product=p).aggregate(
            tq=Sum('quantity'),
            tc=Sum(F('quantity') * F('cost')),
            tp=Sum(F('quantity') * F('price')),
        )
        tq = agg['tq'] or 0
        if tq:
            avg_cost = (agg['tc'] or 0) / tq
            avg_price = (agg['tp'] or 0) / tq
        else:
            avg_cost = p.cost
            avg_price = p.price

        qty = p.stock
        line_cost = Decimal(qty) * Decimal(avg_cost)
        line_sale = Decimal(qty) * Decimal(avg_price)
        grand_cost += line_cost
        grand_sale += line_sale

        rows.append({
            'product': p,
            'qty': qty,
            'avg_cost': avg_cost,
            'avg_price': avg_price,
            'line_cost': line_cost,
            'line_sale': line_sale,
        })

    return render(request, 'salon/inventory_totals.html', {
        'rows': rows,
        'grand_cost': grand_cost,
        'grand_sale': grand_sale,
    })


@login_required
def inventory_totals_pdf(request):
    if not require_access(request, 'can_inv_totals'):
        return redirect('dashboard')
    branch = get_user_branch(request)
    products = Product.objects.filter(is_active=True)
    if branch:
        products = products.filter(branch=branch)
    rows = []
    grand_cost = Decimal('0')
    grand_sale = Decimal('0')
    for p in products.order_by('code', 'name'):
        agg = PurchaseInvoiceItem.objects.filter(product=p).aggregate(
            tq=Sum('quantity'),
            tc=Sum(F('quantity') * F('cost')),
            tp=Sum(F('quantity') * F('price')),
        )
        tq = agg['tq'] or 0
        if tq:
            avg_cost = (agg['tc'] or 0) / tq
            avg_price = (agg['tp'] or 0) / tq
        else:
            avg_cost = p.cost
            avg_price = p.price
        qty = p.stock
        line_cost = Decimal(qty) * Decimal(avg_cost)
        line_sale = Decimal(qty) * Decimal(avg_price)
        grand_cost += line_cost
        grand_sale += line_sale
        rows.append({
            'product': p, 'qty': qty,
            'avg_cost': avg_cost, 'avg_price': avg_price,
            'line_cost': line_cost, 'line_sale': line_sale,
        })
    ctx = {
        'rows': rows, 'grand_cost': grand_cost, 'grand_sale': grand_sale,
        'branch': branch, 'now': timezone.now(),
    }
    return _render_inventory_pdf(
        request, 'salon/inventory_totals_pdf.html', ctx,
        f'inventory_totals_{timezone.now().strftime("%Y%m%d")}.pdf',
    )


@login_required
def stock_movement_add(request):
    if not request.user.can_inventory:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    branch = get_user_branch(request)

    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.branch = branch or Branch.objects.first()
            movement.created_by = request.user
            movement.save()
            log_activity(
                request, ACTION_CREATE, T_STOCK,
                f'{movement.product.name} — {movement.get_movement_type_display()} {movement.quantity}',
                movement.id, movement.branch,
            )
            messages.success(request, "✅ تم تسجيل حركة المخزون بنجاح")
            return redirect('inventory')
    else:
        form = StockMovementForm()
        if branch:
            form.fields['product'].queryset = Product.objects.filter(branch=branch)

    return render(request, 'salon/stock_form.html', {'form': form})


# =============================================================================
# EXPENSES
# =============================================================================

def _expense_voucher_net(qs):
    out = qs.filter(voucher_type='out').aggregate(t=Sum('amount'))['t'] or Decimal('0')
    ret = qs.filter(voucher_type='return').aggregate(t=Sum('amount'))['t'] or Decimal('0')
    return out - ret


def _report_expense_total(branch, start_date, end_date):
    vouchers = ExpenseVoucher.objects.all()
    legacy = Expense.objects.all()
    if branch:
        vouchers = vouchers.filter(branch=branch)
        legacy = legacy.filter(branch=branch)
    if start_date and end_date:
        vouchers = vouchers.filter(date__range=[start_date, end_date])
        legacy = legacy.filter(date__range=[start_date, end_date])
    net = _expense_voucher_net(vouchers)
    old = legacy.aggregate(t=Sum('amount'))['t'] or Decimal('0')
    return net + old


def _expense_voucher_payload(voucher):
    return {
        'success': True,
        'voucher': {
            'id': voucher.id,
            'serial_number': voucher.serial_number,
            'expense_type_id': voucher.expense_type_id,
            'expense_name': voucher.expense_type.name,
            'expense_code': voucher.expense_type.code,
            'payment_method': voucher.payment_method,
            'bank_id': voucher.bank_id,
            'amount': str(voucher.amount),
            'notes': voucher.notes,
        },
    }


def _save_expense_voucher(request, branch, voucher_type):
    data = json.loads(request.body)
    voucher_id = data.get('voucher_id')
    expense_type_id = data.get('expense_type_id')
    payment_method = data.get('payment_method', 'cash')
    bank_id = data.get('bank_id')
    amount = Decimal(str(data.get('amount', 0)))
    notes = data.get('notes', '')

    if not expense_type_id:
        return JsonResponse({'success': False, 'error': 'اختر المصروف'})
    if amount <= 0:
        return JsonResponse({'success': False, 'error': 'أدخل مبلغاً صحيحاً'})
    if payment_method == 'bank' and not bank_id:
        return JsonResponse({'success': False, 'error': 'اختر البنك'})

    expense_type = ExpenseType.objects.get(id=expense_type_id, branch=branch, is_active=True)
    bank = None
    if payment_method == 'bank':
        bank = Bank.objects.get(id=bank_id, is_active=True)

    if voucher_id:
        voucher = ExpenseVoucher.objects.get(id=voucher_id, branch=branch, voucher_type=voucher_type)
        voucher.expense_type = expense_type
        voucher.payment_method = payment_method
        voucher.bank = bank if payment_method == 'bank' else None
        voucher.amount = amount
        voucher.notes = notes
        voucher.save()
        msg = 'تم تحديث السند'
    else:
        voucher = ExpenseVoucher(
            branch=branch,
            voucher_type=voucher_type,
            expense_type=expense_type,
            payment_method=payment_method,
            bank=bank if payment_method == 'bank' else None,
            amount=amount,
            notes=notes,
            created_by=request.user,
        )
        voucher.save()
        msg = f'تم حفظ السند #{voucher.serial_number}'

    log_activity(
        request,
        ACTION_UPDATE if voucher_id else ACTION_CREATE,
        T_EXPENSE_VOUCHER,
        f'#{voucher.serial_number} — {voucher.amount} ج.م',
        voucher.id, branch,
        details=voucher.expense_type.name,
    )

    return JsonResponse({
        'success': True,
        'message': msg,
        'serial_number': voucher.serial_number,
        'voucher_id': voucher.id,
        'next_serial': ExpenseVoucher.next_serial(branch, voucher_type),
    })


@login_required
def expense_list(request):
    if not require_access(request, 'can_expenses'):
        return redirect('dashboard')

    branch = get_user_branch(request)
    qs = ExpenseVoucher.objects.select_related(
        'expense_type', 'bank', 'created_by',
    )
    if branch:
        qs = qs.filter(branch=branch)
    vouchers = qs.order_by('-created_at')[:100]

    return render(request, 'salon/expense_list.html', {'vouchers': vouchers})


@login_required
def expense_type_add(request):
    """تكويد مصروف — كود تلقائي + اسم."""
    if not require_access(request, 'can_expense_types'):
        return redirect('dashboard')

    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    if not branch:
        messages.error(request, "لا يوجد فرع نشط")
        return redirect('expense_list')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action', 'save')
            type_id = data.get('type_id')
            code = str(data.get('code', '')).strip()
            name = data.get('name', '').strip()

            if action == 'delete':
                if not require_access_json(request, 'can_delete_expenses'):
                    return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية الحذف'})
                if not type_id:
                    return JsonResponse({'success': False, 'error': 'اختر مصروفاً أولاً'})
                expense_type = ExpenseType.objects.get(id=type_id, branch=branch)
                ok, msg = expense_type.can_delete_catalog()
                if not ok:
                    return JsonResponse({'success': False, 'error': msg})
                label = f'{expense_type.code} — {expense_type.name}'
                expense_type.delete()
                log_activity(request, ACTION_DELETE, T_EXPENSE_TYPE, label, type_id, branch)
                return JsonResponse({
                    'success': True,
                    'message': 'تم حذف المصروف',
                    'next_code': ExpenseType.next_code(branch),
                })

            if not name:
                return JsonResponse({'success': False, 'error': 'اسم المصروف مطلوب'})

            if type_id:
                expense_type = ExpenseType.objects.get(id=type_id, branch=branch)
                expense_type.name = name
                expense_type.save(update_fields=['name'])
                log_activity(
                    request, ACTION_UPDATE, T_EXPENSE_TYPE,
                    f'{expense_type.code} — {name}', expense_type.id, branch,
                )
                return JsonResponse({'success': True, 'message': 'تم تحديث المصروف'})

            if not code:
                code = ExpenseType.next_code(branch)
            elif ExpenseType.objects.filter(branch=branch, code=code).exists():
                return JsonResponse({'success': False, 'error': f'كود {code} موجود — اضغط Enter لتحميله'})

            ExpenseType.objects.create(branch=branch, code=code, name=name)
            log_activity(request, ACTION_CREATE, T_EXPENSE_TYPE, f'{code} — {name}', None, branch)
            return JsonResponse({
                'success': True,
                'message': f'تم تكويد المصروف {name}',
                'next_code': ExpenseType.next_code(branch),
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'salon/expense_type_form.html', {
        'next_code': ExpenseType.next_code(branch),
    })


@login_required
def expense_type_lookup(request):
    code = request.GET.get('code', '').strip()
    if not code:
        return JsonResponse({'success': False, 'error': 'أدخل كود المصروف'})
    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    expense_type = ExpenseType.objects.filter(branch=branch, code=code).first()
    if not expense_type:
        return JsonResponse({'success': False, 'error': 'مصروف غير موجود'})
    can_del, del_msg = expense_type.can_delete_catalog()
    if not has_perm(request.user, 'can_delete_expenses'):
        can_del, del_msg = False, 'ليس لديك صلاحية الحذف'
    return JsonResponse({
        'success': True,
        'expense_type': {
            'id': expense_type.id,
            'code': expense_type.code,
            'name': expense_type.name,
            'can_delete': can_del,
            'delete_message': del_msg,
        },
    })


@login_required
def expense_out_add(request):
    if not require_access(request, 'can_expense_out'):
        return redirect('dashboard')

    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    if not branch:
        messages.error(request, "لا يوجد فرع نشط")
        return redirect('expense_list')

    if request.method == 'POST':
        try:
            return _save_expense_voucher(request, branch, 'out')
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return _render_expense_voucher_form(request, branch, 'out')


@login_required
def expense_out_lookup(request):
    return _expense_voucher_lookup(request, 'out')


@login_required
@require_POST
def expense_out_delete(request, pk):
    return _expense_voucher_delete(request, pk, 'out')


@login_required
def expense_return_add(request):
    if not require_access(request, 'can_expense_return'):
        return redirect('dashboard')

    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    if not branch:
        messages.error(request, "لا يوجد فرع نشط")
        return redirect('expense_list')

    if request.method == 'POST':
        try:
            return _save_expense_voucher(request, branch, 'return')
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return _render_expense_voucher_form(request, branch, 'return')


@login_required
def expense_return_lookup(request):
    return _expense_voucher_lookup(request, 'return')


@login_required
@require_POST
def expense_return_delete(request, pk):
    return _expense_voucher_delete(request, pk, 'return')


def _render_expense_voucher_form(request, branch, voucher_type):
    expense_types = ExpenseType.objects.filter(branch=branch, is_active=True).order_by('code', 'name')
    banks = get_active_banks()
    is_return = voucher_type == 'return'
    ctx = {
        'expense_types': expense_types,
        'banks': banks,
        'next_serial': ExpenseVoucher.next_serial(branch, voucher_type),
        'voucher_type': voucher_type,
        'is_return': is_return,
        'save_url': '/expenses/return/add/' if is_return else '/expenses/out/add/',
        'lookup_url': '/expenses/return/lookup/' if is_return else '/expenses/out/lookup/',
        'delete_prefix': '/expenses/return/' if is_return else '/expenses/out/',
        'header_bg': 'linear-gradient(135deg,#27ae60,#2ecc71)' if is_return else 'linear-gradient(135deg,#e74c3c,#c0392b)',
    }
    return render(request, 'salon/expense_voucher.html', ctx)


def _expense_voucher_lookup(request, voucher_type):
    q = request.GET.get('serial', '').strip()
    if not q.isdigit():
        return JsonResponse({'success': False, 'error': 'أدخل رقم المسلسل'})
    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    qs = ExpenseVoucher.objects.select_related('expense_type', 'bank')
    if branch:
        qs = qs.filter(branch=branch)
    voucher = qs.filter(serial_number=int(q), voucher_type=voucher_type).first()
    if not voucher:
        return JsonResponse({'success': False, 'error': 'سند غير موجود'})
    return JsonResponse(_expense_voucher_payload(voucher))


def _expense_voucher_delete(request, pk, voucher_type):
    if not require_access_json(request, 'can_delete_expenses'):
        return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية الحذف'})
    branch = get_user_branch(request)
    qs = ExpenseVoucher.objects.filter(pk=pk, voucher_type=voucher_type)
    if branch:
        qs = qs.filter(branch=branch)
    voucher = get_object_or_404(qs)
    serial = voucher.serial_number
    branch = voucher.branch
    voucher.delete()
    label = 'مرتد المصروف' if voucher_type == 'return' else 'المصروف'
    log_activity(
        request, ACTION_DELETE, T_EXPENSE_VOUCHER,
        f'{label} #{serial}', pk, branch,
    )
    return JsonResponse({'success': True, 'message': f'تم حذف {label}'})


@login_required
def expense_add(request):
    return redirect('expense_out_add')

# =============================================================================
# reports_pdf
# =============================================================================


@login_required
def reports_pdf(request):
    if not require_access(request, 'can_reports'):
        return redirect('dashboard')
    branch = get_user_branch(request)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    invoices = Invoice.objects.all()
    
    if not request.user.is_superuser:
        if not branch:
            messages.error(request, "🏪 لم يتم تعيين فرع لهذا المستخدم")
            return redirect('dashboard')
        invoices = invoices.filter(branch=branch)
    
    if start_date and end_date:
        invoices = invoices.filter(created_at__date__range=[start_date, end_date])
    
    total_revenue = invoices.aggregate(total=Sum('final_total'))['total'] or 0
    total_expenses = _report_expense_total(branch if not request.user.is_superuser else None, start_date, end_date)
    net_profit = total_revenue - total_expenses
    total_invoices = invoices.count()

    payment_breakdown = invoices.values('payment_method', 'bank__name').annotate(
        total=Sum('final_total'), count=Count('id')
    ).order_by('-total')

    employee_performance = _employee_performance(invoices)

    # إحصائيات الفروع
    branch_stats = []
    if request.user.is_superuser:
        all_branches = Branch.objects.filter(is_active=True)
        for b in all_branches:
            branch_invoices = Invoice.objects.filter(branch=b)
            if start_date and end_date:
                branch_invoices = branch_invoices.filter(created_at__date__range=[start_date, end_date])
            
            branch_cash = branch_invoices.filter(payment_method='cash').aggregate(total=Sum('final_total'))['total'] or 0
            branch_bank = branch_invoices.filter(payment_method='bank').aggregate(total=Sum('final_total'))['total'] or 0
            
            branch_stats.append({
                'name': b.name,
                'cash': branch_cash,
                'bank': branch_bank,
                'total': branch_cash + branch_bank,
            })
    else:
        if branch:
            branch_invoices = invoices.filter(branch=branch)
            branch_cash = branch_invoices.filter(payment_method='cash').aggregate(total=Sum('final_total'))['total'] or 0
            branch_bank = branch_invoices.filter(payment_method='bank').aggregate(total=Sum('final_total'))['total'] or 0
            
            branch_stats.append({
                'name': branch.name,
                'cash': branch_cash,
                'bank': branch_bank,
                'total': branch_cash + branch_bank,
            })

    total_cash_all = sum(s['cash'] for s in branch_stats)
    total_bank_all = sum(s['bank'] for s in branch_stats)
    grand_total_all = sum(s['total'] for s in branch_stats)

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'total_invoices': total_invoices,
        'payment_breakdown': payment_breakdown,
        'employee_performance': employee_performance,
        'branch_stats': branch_stats,
        'total_cash_all': total_cash_all,
        'total_bank_all': total_bank_all,
        'grand_total_all': grand_total_all,
        'is_superuser': request.user.is_superuser,
        'user': request.user,
        'now': timezone.now(),
    }

    # 🔥 توليد PDF
    html_string = render_to_string('salon/reports_pdf.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    
    # CSS للـ RTL (اختياري)
    css_path = os.path.join(settings.BASE_DIR, 'salon', 'static', 'css', 'pdf_rtl.css')
    if os.path.exists(css_path):
        css = CSS(filename=css_path)
        pdf = html.write_pdf(stylesheets=[css])
    else:
        pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="report_{timezone.now().strftime("%Y%m%d")}.pdf"'
    return response  # ✅ return واحدة بس


# =============================================================================
# REPORTS
# =============================================================================

@login_required
def reports(request):
    if not require_access(request, 'can_reports'):
        return redirect('dashboard')
    branch = get_user_branch(request)
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    invoices = Invoice.objects.all()
    
    if not request.user.is_superuser:
        if not branch:
            messages.error(request, "🏪 لم يتم تعيين فرع لهذا المستخدم")
            return redirect('dashboard')
        invoices = invoices.filter(branch=branch)
    
    if start_date and end_date:
        invoices = invoices.filter(created_at__date__range=[start_date, end_date])
    
    # التوتال العام
    total_revenue = invoices.aggregate(total=Sum('final_total'))['total'] or 0
    total_expenses = _report_expense_total(branch if not request.user.is_superuser else None, start_date, end_date)
    net_profit = total_revenue - total_expenses
    total_invoices = invoices.count()

    # طرق الدفع
    payment_breakdown = invoices.values('payment_method', 'bank__name').annotate(
        total=Sum('final_total'),
        count=Count('id')
    ).order_by('-total')

    # أداء الموظفين
    employee_performance = _employee_performance(invoices)

    # 🔥 إحصائيات الفروع
    branch_stats = []
    
    if request.user.is_superuser:
        all_branches = Branch.objects.filter(is_active=True)
        for b in all_branches:
            # فلترة الفواتير بالفرع والتاريخ
            branch_invoices = Invoice.objects.filter(branch=b)
            if start_date and end_date:
                branch_invoices = branch_invoices.filter(created_at__date__range=[start_date, end_date])
            
            # كاش
            branch_cash = branch_invoices.filter(payment_method='cash').aggregate(
                total=Sum('final_total')
            )['total'] or 0
            
            # بنك
            branch_bank = branch_invoices.filter(payment_method='bank').aggregate(
                total=Sum('final_total')
            )['total'] or 0
            
            branch_total = branch_cash + branch_bank
            
            branch_stats.append({
                'name': b.name,
                'cash': branch_cash,
                'bank': branch_bank,
                'total': branch_total,
            })
    else:
        if branch:
            branch_invoices = invoices.filter(branch=branch)
            
            branch_cash = branch_invoices.filter(payment_method='cash').aggregate(
                total=Sum('final_total')
            )['total'] or 0
            
            branch_bank = branch_invoices.filter(payment_method='bank').aggregate(
                total=Sum('final_total')
            )['total'] or 0
            
            branch_total = branch_cash + branch_bank
            
            branch_stats.append({
                'name': branch.name,
                'cash': branch_cash,
                'bank': branch_bank,
                'total': branch_total,
            })

    # 🔥 حساب التوتال الكلي هنا - بعد ما branch_stats تتملى
    total_cash_all = sum(stat['cash'] for stat in branch_stats)
    total_bank_all = sum(stat['bank'] for stat in branch_stats)
    grand_total_all = sum(stat['total'] for stat in branch_stats)

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'total_invoices': total_invoices,
        'payment_breakdown': payment_breakdown,
        'employee_performance': employee_performance,
        'branch_stats': branch_stats,
        'total_cash_all': total_cash_all,        # 🔥
        'total_bank_all': total_bank_all,        # 🔥
        'grand_total_all': grand_total_all,      # 🔥
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'salon/reports.html', context)


@login_required
def activity_log(request):
    """سجل الحركات — إنشاء / تعديل / حذف / إلغاء."""
    if not can_view_activity_log(request.user):
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    branch = get_user_branch(request)
    today = timezone.localdate().isoformat()
    start_date = request.GET.get('start_date') or today
    end_date = request.GET.get('end_date') or today

    logs = ActivityLog.objects.select_related('user', 'branch')
    if not request.user.is_superuser:
        if not branch:
            messages.error(request, "🏪 لم يتم تعيين فرع لهذا المستخدم")
            return redirect('dashboard')
        logs = logs.filter(branch=branch)

    logs = logs.filter(created_at__date__range=[start_date, end_date])

    counts = {
        'create': logs.filter(action=ActivityLog.ACTION_CREATE).count(),
        'update': logs.filter(action=ActivityLog.ACTION_UPDATE).count(),
        'delete': logs.filter(action=ActivityLog.ACTION_DELETE).count(),
        'void': logs.filter(action=ActivityLog.ACTION_VOID).count(),
    }

    return render(request, 'salon/activity_log.html', {
        'logs': logs[:500],
        'start_date': start_date,
        'end_date': end_date,
        'counts': counts,
        'total_count': logs.count(),
        'is_superuser': request.user.is_superuser,
    })


@login_required
def account_statement(request):
    """كشف الحسابات — نقدية وبنوك."""
    if not require_access(request, 'can_report_statement'):
        return redirect('dashboard')

    branch = get_statement_branch(request)
    if branch is None and not request.user.can_see_all_branches:
        user_branch = get_user_branch(request)
        if not user_branch:
            messages.error(request, "🏪 لم يتم تعيين فرع لهذا المستخدم")
            return redirect('dashboard')
        branch = user_branch

    today = timezone.localdate().isoformat()
    start_date = request.GET.get('start_date') or today
    end_date = request.GET.get('end_date') or today
    statement_type = request.GET.get('type', 'cash')
    bank_id = request.GET.get('bank', '').strip()

    if statement_type == 'bank':
        data = build_bank_statement(
            branch, start_date, end_date,
            bank_id=int(bank_id) if bank_id.isdigit() else None,
        )
    elif statement_type == 'transfer':
        data = build_transfer_statement(
            branch, start_date, end_date,
            bank_id=int(bank_id) if bank_id.isdigit() else None,
        )
    else:
        statement_type = 'cash'
        data = build_cash_statement(branch, start_date, end_date)

    branches = Branch.objects.filter(is_active=True) if request.user.can_see_all_branches else []

    return render(request, 'salon/account_statement.html', {
        'statement_type': statement_type,
        'rows': data['rows'],
        'total_in': data['total_in'],
        'total_out': data['total_out'],
        'balance': data['balance'],
        'start_date': start_date,
        'end_date': end_date,
        'branches': branches,
        'banks': get_active_banks(),
        'show_branch_filter': request.user.can_see_all_branches,
        'selected_branch_id': request.GET.get('branch', ''),
        'selected_bank_id': bank_id,
    })


@login_required
@require_POST
def account_transfer_save(request):
    """تحويل بين النقدية والبنك."""
    if not require_access_json(request, 'can_report_statement'):
        return JsonResponse({'success': False, 'error': 'غير مصرح'})

    try:
        data = json.loads(request.body)
        direction = data.get('direction', '').strip()
        bank_id = data.get('bank_id')
        amount = Decimal(str(data.get('amount', 0)))
        notes = (data.get('notes') or '').strip()
        transfer_date = (data.get('date') or '').strip() or timezone.localdate().isoformat()

        if direction not in (
            AccountTransfer.DIRECTION_CASH_TO_BANK,
            AccountTransfer.DIRECTION_BANK_TO_CASH,
        ):
            return JsonResponse({'success': False, 'error': 'اتجاه التحويل غير صالح'})
        if not bank_id:
            return JsonResponse({'success': False, 'error': 'اختر البنك'})
        if amount <= 0:
            return JsonResponse({'success': False, 'error': 'المبلغ يجب أن يكون أكبر من صفر'})

        bank = get_object_or_404(Bank, id=bank_id, is_active=True)

        branch = get_user_branch(request)
        if not branch:
            branch_param = data.get('branch_id') or request.GET.get('branch')
            if branch_param and getattr(request.user, 'can_see_all_branches', False):
                branch = get_object_or_404(Branch, id=int(branch_param), is_active=True)
            else:
                branch = Branch.objects.filter(is_active=True).first()

        if not branch:
            return JsonResponse({'success': False, 'error': 'لم يتم تحديد فرع'})

        from datetime import datetime
        date_obj = datetime.strptime(transfer_date, '%Y-%m-%d').date()

        transfer = AccountTransfer.objects.create(
            branch=branch,
            direction=direction,
            bank=bank,
            amount=amount,
            notes=notes,
            date=date_obj,
            created_by=request.user,
        )

        log_activity(
            request, ACTION_CREATE, T_ACCOUNT_TRANSFER,
            f'#{transfer.serial_number} {transfer.get_direction_display()} — {bank.name} — {amount}',
            entity_id=transfer.id,
            branch=branch,
        )

        return JsonResponse({
            'success': True,
            'serial': transfer.serial_number,
            'message': f'تم التحويل #{transfer.serial_number}',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# =============================================================================
# SERVICES
# =============================================================================

@login_required
def service_list(request):
    if not require_access(request, 'can_services'):
        return redirect('dashboard')
    services = get_branch_queryset(request, Service, 'code')
    return render(request, 'salon/service_list.html', {'services': services})


@login_required
def service_add(request):
    """تكويد خدمة — مسلسل + اسم + سعر + نشط."""
    if not require_access(request, 'can_services'):
        return redirect('dashboard')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action', 'save')
            service_id = data.get('service_id')
            code = str(data.get('code', '')).strip()
            name = data.get('name', '').strip()
            price = Decimal(str(data.get('price', 0)))
            is_active = bool(data.get('is_active', True))

            if action == 'delete':
                if not require_access_json(request, 'can_delete_services'):
                    return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية الحذف'})
                if not service_id:
                    return JsonResponse({'success': False, 'error': 'اختر خدمة أولاً'})
                service = Service.objects.get(id=service_id)
                ok, msg = service.can_delete_catalog()
                if not ok:
                    return JsonResponse({'success': False, 'error': msg})
                label = f'{service.code} — {service.name}'
                service.delete()
                log_activity(request, ACTION_DELETE, T_SERVICE, label, service_id, None)
                return JsonResponse({
                    'success': True,
                    'message': 'تم حذف الخدمة',
                    'next_code': Service.next_code(),
                })

            if not name:
                return JsonResponse({'success': False, 'error': 'اسم الخدمة مطلوب'})
            if price < 0:
                return JsonResponse({'success': False, 'error': 'أدخل سعراً صحيحاً'})

            if service_id:
                service = Service.objects.get(id=service_id)
                service.name = name
                service.price = price
                service.is_active = is_active
                service.save(update_fields=['name', 'price', 'is_active'])
                log_activity(
                    request, ACTION_UPDATE, T_SERVICE,
                    f'{service.code} — {name}', service.id, None,
                )
                return JsonResponse({'success': True, 'message': 'تم تحديث الخدمة'})

            if not code:
                code = Service.next_code()
            elif Service.objects.filter(code=code).exists():
                return JsonResponse({'success': False, 'error': f'مسلسل {code} موجود — اضغط Enter لتحميله'})

            Service.objects.create(
                code=code, name=name, price=price,
                is_active=is_active, cost=0, duration=30,
            )
            log_activity(request, ACTION_CREATE, T_SERVICE, f'{code} — {name}', None, None)
            return JsonResponse({
                'success': True,
                'message': f'تم تكويد الخدمة {name}',
                'next_code': Service.next_code(),
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'salon/service_form.html', {
        'next_code': Service.next_code(),
    })


@login_required
def service_lookup(request):
    code = request.GET.get('code', '').strip()
    if not code:
        return JsonResponse({'success': False, 'error': 'أدخل المسلسل'})
    service = Service.objects.filter(code=code).first()
    if not service:
        return JsonResponse({'success': False, 'error': 'خدمة غير موجودة'})
    can_del, del_msg = service.can_delete_catalog()
    if not has_perm(request.user, 'can_delete_services'):
        can_del, del_msg = False, 'ليس لديك صلاحية الحذف'
    return JsonResponse({
        'success': True,
        'service': {
            'id': service.id,
            'code': service.code,
            'name': service.name,
            'price': str(service.price),
            'is_active': service.is_active,
            'can_delete': can_del,
            'delete_message': del_msg,
        },
    })


# =============================================================================
# EMPLOYEES
# =============================================================================

@login_required
def employee_list(request):
    if not require_access(request, 'can_employees'):
        return redirect('dashboard')
    employees = get_branch_queryset(request, Employee, 'serial_number')
    return render(request, 'salon/employee_list.html', {'employees': employees})


@login_required
def employee_add(request):
    """تكويد موظف — كود + اسم + نشط."""
    if not require_access(request, 'can_employees'):
        return redirect('dashboard')
    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    if not branch:
        messages.error(request, "لا يوجد فرع نشط")
        return redirect('dashboard')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action', 'save')
            employee_id = data.get('employee_id')
            code = str(data.get('code', '')).strip()
            name = data.get('name', '').strip()
            is_active = bool(data.get('is_active', True))

            if action == 'delete':
                if not require_access_json(request, 'can_delete_employees'):
                    return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية الحذف'})
                if not employee_id:
                    return JsonResponse({'success': False, 'error': 'اختر موظفاً أولاً'})
                employee = Employee.objects.get(id=employee_id)
                if not request.user.is_superuser and employee.branch != branch:
                    return JsonResponse({'success': False, 'error': 'غير مصرح'})
                ok, msg = employee.can_delete_catalog()
                if not ok:
                    return JsonResponse({'success': False, 'error': msg})
                label = f'{employee.serial_number} — {employee.name}'
                employee.delete()
                log_activity(request, ACTION_DELETE, T_EMPLOYEE, label, employee_id, employee.branch)
                return JsonResponse({
                    'success': True,
                    'message': 'تم حذف الموظف',
                    'next_code': Employee.next_code(branch),
                })

            if not name:
                return JsonResponse({'success': False, 'error': 'اسم الموظف مطلوب'})

            if employee_id:
                employee = Employee.objects.get(id=employee_id)
                if not request.user.is_superuser and employee.branch != branch:
                    return JsonResponse({'success': False, 'error': 'غير مصرح'})
                employee.name = name
                employee.is_active = is_active
                employee.save(update_fields=['name', 'is_active'])
                log_activity(
                    request, ACTION_UPDATE, T_EMPLOYEE,
                    f'{employee.serial_number} — {name}', employee.id, employee.branch,
                )
                return JsonResponse({'success': True, 'message': 'تم تحديث الموظف'})

            if not code:
                code = Employee.next_code(branch)
            elif Employee.objects.filter(branch=branch, serial_number=code).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'كود {code} موجود — اضغط Enter لتحميله',
                })

            Employee.objects.create(
                branch=branch,
                serial_number=code,
                name=name,
                is_active=is_active,
                hire_date=timezone.localdate(),
            )
            log_activity(request, ACTION_CREATE, T_EMPLOYEE, f'{code} — {name}', None, branch)
            return JsonResponse({
                'success': True,
                'message': f'تم تكويد الموظف {name}',
                'next_code': Employee.next_code(branch),
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'salon/employee_form.html', {
        'next_code': Employee.next_code(branch),
    })


@login_required
def employee_lookup(request):
    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    code = request.GET.get('code', '').strip()
    if not code:
        return JsonResponse({'success': False, 'error': 'أدخل كود الموظف'})
    if not branch:
        return JsonResponse({'success': False, 'error': 'لا يوجد فرع'})
    employee = Employee.objects.filter(branch=branch, serial_number=code).first()
    if not employee:
        return JsonResponse({'success': False, 'error': 'موظف غير موجود'})
    can_del, del_msg = employee.can_delete_catalog()
    if not has_perm(request.user, 'can_delete_employees'):
        can_del, del_msg = False, 'ليس لديك صلاحية الحذف'
    return JsonResponse({
        'success': True,
        'employee': {
            'id': employee.id,
            'code': employee.serial_number,
            'name': employee.name,
            'is_active': employee.is_active,
            'can_delete': can_del,
            'delete_message': del_msg,
        },
    })


# =============================================================================
# PRODUCTS
# =============================================================================

@login_required
def product_list(request):
    products = get_branch_queryset(request, Product, 'name')
    return render(request, 'salon/product_list.html', {'products': products})


@login_required
def product_add(request):
    branch = get_user_branch(request)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.branch = branch or Branch.objects.first()
            product.save()
            log_activity(
                request, ACTION_CREATE, T_PRODUCT,
                f'{product.code} — {product.name}', product.id, product.branch,
            )
            messages.success(request, f"✅ تم إضافة المنتج {product.name} بنجاح")
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'salon/product_form.html', {'form': form})


# =============================================================================
# CUSTOMERS
# =============================================================================

@login_required
def customer_list(request):
    if not require_access(request, 'can_customers'):
        return redirect('dashboard')
    customers = get_branch_queryset(request, Customer)
    return render(request, 'salon/customer_list.html', {'customers': customers})


@login_required
def customer_add(request):
    if not require_access(request, 'can_customers'):
        return redirect('dashboard')
    branch = get_user_branch(request)

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.branch = branch or Branch.objects.first()
            customer.save()
            log_activity(
                request, ACTION_CREATE, T_CUSTOMER,
                f'{customer.name} — {customer.phone}', customer.id, customer.branch,
            )
            messages.success(request, f"✅ تم إضافة العميل {customer.name} بنجاح")
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'salon/customer_form.html', {'form': form})


# =============================================================================
# SETTINGS
# =============================================================================

@login_required
def settings_view(request):
    if not request.user.can_settings and not request.user.is_superuser:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    salon_settings = SalonSettings.get()

    if request.method == 'POST':
        form_type = request.POST.get('form_type', 'salon')
        if form_type == 'salon':
            salon_settings.salon_name = request.POST.get('salon_name', '').strip() or 'صالون برو'
            salon_settings.phone = request.POST.get('phone', '').strip()
            salon_settings.address = request.POST.get('address', '').strip()
            if request.FILES.get('logo'):
                salon_settings.logo = request.FILES['logo']
            salon_settings.save()
            log_activity(request, ACTION_UPDATE, T_SETTINGS, salon_settings.salon_name)
            messages.success(request, "✅ تم حفظ إعدادات الصالون")
        elif form_type == 'restore':
            if not request.user.is_superuser:
                messages.error(request, "⛔ الاستعادة متاحة للمدير فقط")
                return redirect('settings')
            if request.POST.get('confirm_restore') != 'RESTORE':
                messages.error(request, "❌ اكتب RESTORE للتأكيد")
                return redirect('settings')
            backup_file = request.FILES.get('backup_file')
            if not backup_file:
                messages.error(request, "❌ اختر ملف SQL")
                return redirect('settings')
            if not backup_file.name.lower().endswith('.sql'):
                messages.error(request, "❌ الملف يجب أن يكون .sql")
                return redirect('settings')
            try:
                restore_backup_sql(backup_file)
                log_activity(request, ACTION_UPDATE, T_BACKUP, 'استعادة قاعدة البيانات')
                messages.success(request, "✅ تمت استعادة قاعدة البيانات بنجاح")
            except Exception as e:
                messages.error(request, f"❌ فشل الاستعادة: {e}")
            return redirect('settings')

    branches = Branch.objects.all() if request.user.is_superuser else Branch.objects.filter(id=get_user_branch(request).id) if get_user_branch(request) else Branch.objects.none()
    users = User.objects.all().order_by('user_code', 'username')
    if not request.user.is_superuser:
        users = users.filter(branch=get_user_branch(request))
    banks = get_active_banks() if request.user.is_superuser else get_active_banks()

    last_backup = latest_backup_info()

    return render(request, 'salon/settings.html', {
        'branches': branches,
        'users': users,
        'banks': banks,
        'settings': salon_settings,
        'last_backup': last_backup,
    })


@login_required
def settings_backup(request):
    if not request.user.can_settings and not request.user.is_superuser:
        return HttpResponse('Forbidden', status=403)
    try:
        filepath = create_backup_sql()
        with open(filepath, 'rb') as f:
            content = f.read()
        response = HttpResponse(content, content_type='application/sql')
        response['Content-Disposition'] = f'attachment; filename="{filepath.name}"'
        return response
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'fetch' or 'fetch' in request.META.get('HTTP_SEC_FETCH_MODE', ''):
            return HttpResponse(str(e), status=500, content_type='text/plain; charset=utf-8')
        messages.error(request, f"❌ {e}")
        return redirect('settings')


# =============================================================================
# USERS
# =============================================================================

# دالة مساعدة للتحقق من صلاحية المستخدم على إدارة المستخدمين وحماية الفروع
def check_user_permission(request, target_user=None):
    # إذا لم يكن سوبر يوزر وليس لديه صلاحية إدارة المستخدمين -> مرفوض
    if not request.user.is_superuser and not (
        getattr(request.user, 'can_users', False) or getattr(request.user, 'can_settings', False)
    ):
        return False
    
    # حماية الفروع: لو مش سوبر يوزر وبيحاول يوصل لمستخدم في فرع تاني -> مرفوض
    if target_user and not request.user.is_superuser:
        user_branch = get_user_branch(request)
        if target_user.branch != user_branch:
            return False
            
    return True


USER_ACCESS_FIELDS = ()  # legacy — use permissions.apply_user_permissions


def _apply_user_access(user, data):
    apply_user_permissions(user, data)
    if 'is_active' in data:
        user.is_active = bool(data.get('is_active', True))


def require_access(request, perm, redirect_to='dashboard'):
    if request.user.is_superuser:
        return True
    if not has_perm(request.user, perm):
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return False
    return True


def require_access_json(request, perm):
    if request.user.is_superuser:
        return True
    if not has_perm(request.user, perm):
        return False
    return True


def can_view_activity_log(user):
    return user.is_superuser or has_perm(user, 'can_report_activity')


@login_required
def user_list(request):
    if not check_user_permission(request):
        messages.error(request, "⛔ ليس لديك صلاحية الوصول لإدارة المستخدمين")
        return redirect('dashboard')

    # السوبر يوزر يرى الجميع، مستخدم الفرع يرى مستخدمي فرعه فقط
    if request.user.is_superuser:
        users = User.objects.all()
    else:
        users = User.objects.filter(branch=get_user_branch(request))
        
    return render(request, 'salon/user_list.html', {'users': users})


@login_required
def user_add(request):
    """تكويد مستخدم — كود + إنشاء / تعديل صلاحيات وكلمة المرور."""
    if not check_user_permission(request):
        messages.error(request, "⛔ ليس لديك صلاحية الوصول لإدارة المستخدمين")
        return redirect('settings')

    if request.user.is_superuser:
        branches = Branch.objects.filter(is_active=True)
    else:
        user_branch = get_user_branch(request)
        branches = Branch.objects.filter(id=user_branch.id) if user_branch else Branch.objects.none()

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action', 'save')
            user_id = data.get('user_id')

            if action == 'delete':
                if not user_id:
                    return JsonResponse({'success': False, 'error': 'اختر مستخدماً أولاً'})
                user_obj = User.objects.get(id=user_id)
                if not check_user_permission(request, target_user=user_obj):
                    return JsonResponse({'success': False, 'error': 'غير مصرح'})
                if user_obj == request.user:
                    return JsonResponse({'success': False, 'error': 'لا يمكنك حذف حسابك الحالي'})
                ok, msg = user_obj.can_delete_account()
                if not ok:
                    return JsonResponse({'success': False, 'error': msg})
                uname = user_obj.username
                ubranch = user_obj.branch
                user_obj.delete()
                log_activity(request, ACTION_DELETE, T_USER, uname, user_id, ubranch)
                return JsonResponse({
                    'success': True,
                    'message': 'تم حذف المستخدم',
                    'next_code': User.next_code(),
                })

            if user_id:
                user_obj = User.objects.get(id=user_id)
                if not check_user_permission(request, target_user=user_obj):
                    return JsonResponse({'success': False, 'error': 'غير مصرح'})
                password = data.get('password', '').strip()
                if password:
                    user_obj.set_password(password)
                if not user_obj.is_superuser:
                    _apply_user_access(user_obj, data)
                user_obj.save()
                log_activity(
                    request, ACTION_UPDATE, T_USER,
                    user_obj.username, user_obj.id, user_obj.branch,
                )
                return JsonResponse({'success': True, 'message': 'تم تحديث المستخدم'})

            username = data.get('username', '').strip()
            first_name = data.get('first_name', '').strip()
            last_name = data.get('last_name', '').strip()
            password = data.get('password', '').strip()
            branch_id = data.get('branch_id')
            user_code = str(data.get('user_code', '')).strip()

            if not username or not first_name or not password:
                return JsonResponse({'success': False, 'error': 'اسم المستخدم والاسم وكلمة المرور مطلوبة'})
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'error': 'اسم المستخدم موجود مسبقاً'})
            if not user_code:
                user_code = User.next_code()
            elif User.objects.filter(user_code=user_code).exists():
                return JsonResponse({'success': False, 'error': f'كود {user_code} موجود — Enter لتحميله'})

            if not request.user.is_superuser:
                branch = get_user_branch(request)
            else:
                branch = Branch.objects.filter(id=branch_id).first() if branch_id else None
            if not branch:
                return JsonResponse({'success': False, 'error': 'اختر الفرع'})

            user_obj = User(
                user_code=user_code,
                username=username,
                first_name=first_name,
                last_name=last_name,
                email='',
                branch=branch,
            )
            _apply_user_access(user_obj, data)
            user_obj.set_password(password)
            user_obj.save()
            log_activity(
                request, ACTION_CREATE, T_USER,
                username, user_obj.id, branch,
            )
            return JsonResponse({
                'success': True,
                'message': f'تم تكويد المستخدم {username}',
                'next_code': User.next_code(),
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'salon/user_form.html', {
        'branches': branches,
        'next_code': User.next_code(),
        'permission_groups': PERMISSION_GROUPS,
    })


@login_required
def user_lookup(request):
    if not check_user_permission(request):
        return JsonResponse({'success': False, 'error': 'غير مصرح'})
    code = request.GET.get('code', '').strip()
    if not code:
        return JsonResponse({'success': False, 'error': 'أدخل كود المستخدم'})
    user_obj = User.objects.filter(user_code=code).first()
    if not user_obj:
        return JsonResponse({'success': False, 'error': 'مستخدم غير موجود'})
    if not check_user_permission(request, target_user=user_obj):
        return JsonResponse({'success': False, 'error': 'غير مصرح'})
    can_del, del_msg = user_obj.can_delete_account()
    payload = user_permissions_payload(user_obj)
    payload.update({
        'id': user_obj.id,
        'user_code': user_obj.user_code,
        'username': user_obj.username,
        'full_name': user_obj.get_full_name() or user_obj.username,
        'first_name': user_obj.first_name,
        'last_name': user_obj.last_name,
        'branch_name': str(user_obj.branch) if user_obj.branch else '—',
        'is_superuser': user_obj.is_superuser,
        'can_delete': can_del,
        'delete_message': del_msg,
    })
    return JsonResponse({
        'success': True,
        'user': payload,
    })


@login_required
def user_edit(request, pk):
    return redirect('user_add')


@login_required
@require_POST
def user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if not check_user_permission(request, target_user=user_obj):
        return JsonResponse({'success': False, 'error': 'غير مصرح'})
    if user_obj == request.user:
        return JsonResponse({'success': False, 'error': 'لا يمكنك حذف حسابك الحالي'})
    ok, msg = user_obj.can_delete_account()
    if not ok:
        return JsonResponse({'success': False, 'error': msg})
    username = user_obj.username
    ubranch = user_obj.branch
    user_obj.delete()
    log_activity(request, ACTION_DELETE, T_USER, username, pk, ubranch)
    return JsonResponse({'success': True, 'message': f'تم حذف المستخدم {username}'})

# =============================================================================
# BRANCHES
# =============================================================================

@login_required
def branch_list(request):
    if not request.user.is_superuser:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    branches = Branch.objects.all()
    return render(request, 'salon/branch_list.html', {'branches': branches})


@login_required
def branch_add(request):
    if not request.user.is_superuser:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ تم إنشاء الفرع بنجاح")
            return redirect('branch_list')
    else:
        form = BranchForm()

    return render(request, 'salon/branch_form.html', {'form': form})


# =============================================================================
# BANKS
# =============================================================================

@login_required
def bank_list(request):
    if not request.user.can_settings and not request.user.is_superuser:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    banks = get_active_banks()

    return render(request, 'salon/bank_list.html', {'banks': banks})


@login_required
def bank_add(request):
    if not request.user.can_settings and not request.user.is_superuser:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        account_number = request.POST.get('account_number', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        if not name:
            messages.error(request, "اسم البنك مطلوب")
            return redirect('bank_add')
        Bank.objects.create(
            name=name,
            account_number=account_number,
            branch=None,
            is_active=is_active,
        )
        messages.success(request, "✅ تم إضافة البنك — يظهر في كل الفروع")
        return redirect('settings')

    return render(request, 'salon/bank_form.html')


# =============================================================================
# PRINTING - Queue Tickets & Invoices
# =============================================================================

@login_required
def print_simple_queue_receipt(request):
    """طباعة رقم دور بسيط — نفس إعدادات الهيدر/الفوتر."""
    number = request.GET.get('number', '').strip()
    if not number.isdigit():
        return redirect('booking_list')

    branch_name = request.GET.get('branch', '').strip()
    customer_name = request.GET.get('customer', 'عميل').strip() or 'عميل'
    date_str = request.GET.get('date', timezone.localdate().isoformat())
    time_str = request.GET.get('time', timezone.localtime().strftime('%H:%M'))

    context = {
        'queue_number': int(number),
        'customer_name': customer_name,
        'branch_name': branch_name,
        'now': timezone.now(),
        'config': SalonSettings.get().print_config(request),
        'display_date': date_str,
        'display_time': time_str,
    }
    return render(request, 'salon/queue_receipt.html', context)


@login_required
def print_queue_ticket(request, pk):
    """Print a queue/waiting ticket"""
    booking = get_object_or_404(Booking, pk=pk)

    # Get services names
    services = [s.name for s in booking.services.all()]

    # Calculate estimated total
    estimated_total = sum(s.price for s in booking.services.all())

    context = {
        'booking': booking,
        'queue_number': booking.queue_number,
        'customer_name': booking.customer_name,
        'employee_name': (
            booking.employee.name if booking.employee
            else (booking.barber.get_full_name() if booking.barber else '')
        ),
        'services': services,
        'estimated_total': estimated_total,
        'now': timezone.now(),
        'config': SalonSettings.get().print_config(request),
    }

    return render(request, 'salon/queue_receipt.html', context)


@login_required
def print_invoice_receipt(request, pk):
    """Print sales invoice receipt"""
    invoice = get_object_or_404(Invoice, pk=pk)
    items = invoice.items.all()

    context = {
        'invoice': invoice,
        'items': items,
        'config': SalonSettings.get().print_config(request),
    }

    return render(request, 'salon/invoice_receipt.html', context)


@login_required
@require_POST
def print_direct_queue(request, pk):
    """Direct print queue ticket to Windows printer"""
    try:
        from .printer import print_queue_ticket
        booking = get_object_or_404(Booking, pk=pk)
        services = [s.name for s in booking.services.all()]
        estimated_total = sum(s.price for s in booking.services.all())

        success, message = print_queue_ticket(
            queue_number=booking.queue_number,
            customer_name=booking.customer_name,
            employee_name=(
                booking.employee.name if booking.employee
                else (booking.barber.get_full_name() if booking.barber else '')
            ),
            services=services,
            estimated_total=estimated_total,
            request=request,
        )

        return JsonResponse({'success': success, 'message': message})
    except ImportError:
        # printer.py not installed - return graceful error
        return JsonResponse({
            'success': False, 
            'message': 'Direct printer not configured. Use browser print instead.',
            'fallback_url': f'/booking/{pk}/print/'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_POST
def print_direct_invoice(request, pk):
    """Direct print invoice to Windows printer"""
    try:
        from .printer import print_invoice_receipt
        invoice = get_object_or_404(Invoice, pk=pk)
        items = invoice.items.all()

        success, message = print_invoice_receipt(invoice, items, request=request)

        return JsonResponse({'success': success, 'message': message})
    except ImportError:
        # printer.py not installed - return graceful error with fallback
        return JsonResponse({
            'success': False,
            'message': 'Direct printer not configured. Use browser print instead.',
            'fallback_url': f'/invoice/{pk}/receipt/'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# =============================================================================
# API
# =============================================================================

@login_required
def api_search_customer(request):
    phone = request.GET.get('phone', '')
    branch = get_user_branch(request)

    customers = Customer.objects.filter(phone__icontains=phone)
    if branch:
        customers = customers.filter(branch=branch)

    customer = customers.first()
    if customer:
        return JsonResponse({
            'found': True,
            'name': customer.name,
            'phone': customer.phone,
            'visits': customer.visits_count,
            'total_spent': float(customer.total_spent),
        })
    return JsonResponse({'found': False})


@login_required
def api_service_search(request):
    q = request.GET.get('q', '')
    branch = get_user_branch(request)

    services = Service.objects.filter(name__icontains=q, is_active=True)
    if branch:
        services = services.filter(branch=branch)

    return JsonResponse({
        'services': [
            {'id': s.id, 'name': s.name, 'price': float(s.price), 'duration': s.duration}
            for s in services[:10]
        ]
    })