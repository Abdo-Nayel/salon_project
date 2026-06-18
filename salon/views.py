"""
Salon Pro Views - Complete System
"""
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
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


from django_weasyprint import WeasyTemplateView
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
                
            message = f"💈 *Salon Pro*\n\nعزيزي العميل، تم إصدار فاتورتك بنجاح.\n📄 فاتورة رقم: #{invoice_number}\n🔗 لمشاهدة الفاتورة: {request.build_absolute_uri(f'/invoice/{invoice_id}/receipt/')}\n\nشكراً لزيارتك! 🙏"

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

import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Service, User, Bank, Invoice, InvoiceItem, Branch, Customer

# افترضنا وجود هذه الدوال المساعدة في مشروعك
def get_user_branch(request):
    # كود جلب فرع المستخدم الحالي
    return getattr(request.user, 'branch', None)

@login_required
def pos(request):
    if not request.user.can_pos:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    branch = get_user_branch(request)
    if not branch and not request.user.is_superuser:
        messages.error(request, "🏪 لم يتم تعيين فرع لهذا المستخدم")
        return redirect('dashboard')

    # جلب البيانات الأساسية بناءً على الفرع
    if branch:
        services = Service.objects.filter(is_active=True)
        barbers = User.objects.filter(is_barber=True, branch=branch, is_active=True)
        banks = Bank.objects.filter(branch=branch, is_active=True)
    else:
        services = Service.objects.filter(is_active=True)
        barbers = User.objects.filter(is_barber=True, is_active=True)
        banks = Bank.objects.filter(is_active=True)

    if request.method == 'POST':
        data = json.loads(request.body)
        items = data.get('items', [])
        invoice_id = data.get('invoice_id')
        booking_id = data.get('booking_id')

        if not items:
            return JsonResponse({'success': False, 'error': 'السلة فارغة!'})

        try:
            # استخدام atomic لمنع مشاكل الـ Race Condition وتداخل طلبات الـ Multi-user
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
                    
                    # خصم القيمة القديمة من حساب العميل قبل التعديل لإعادة الاحتساب بدقة
                    if invoice.customer:
                        invoice.customer.total_spent -= invoice.final_total
                        invoice.customer.save()
                    
                    # حذف العناصر القديمة لإعادة بنائها حسب التعديل الجديد
                    invoice.items.all().delete()
                else:
                    # حالة فاتورة جديدة تماماً
                    invoice = Invoice()
                    invoice.branch = branch or Branch.objects.first()
                    invoice.created_by = request.user

                # إدخال وتحديث بيانات العميل
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

                # إدخال وتحديث الحلاق
                barber_id = data.get('barber')
                if barber_id:
                    invoice.barber = User.objects.get(id=barber_id)
                else:
                    invoice.barber = None

                # طريقة الدفع والبنك
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
                
                # حفظ مبدئي لتوليد السيريال والـ ID في قاعدة البيانات إن كانت جديدة
                invoice.save()

                # إعادة بناء عناصر الفاتورة واحتساب المجموع
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
                invoice.save()  # الحفظ النهائي (يقوم موديل Invoice باحتساب final_total تلقائياً في دالة save)

                # تحديث إحصائياتspent العميل الإجمالية بعد الحفظ
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
        'barbers': barbers,
        'banks': banks,
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
    bookings = get_branch_queryset(request, Booking, 'queue_number')
    return render(request, 'salon/booking_list.html', {'bookings': bookings})


@login_required
def booking_add(request):
    branch = get_user_branch(request) or Branch.objects.filter(is_active=True).first()
    if not branch:
        messages.error(request, "لا يوجد فرع نشط")
        return redirect('dashboard')

    services = Service.objects.filter(is_active=True)
    barbers = User.objects.filter(is_barber=True, branch=branch, is_active=True)

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
            barber_id = data.get('barber')
            if barber_id:
                booking.barber = User.objects.filter(id=barber_id).first()
            booking.save()

            service_ids = [item['id'] for item in items]
            booking.services.set(Service.objects.filter(id__in=service_ids))

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
        'barbers': barbers,
    })

@login_required
@require_POST
def booking_status(request, pk):
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
    return JsonResponse({'success': True})



@login_required
@require_POST
def print_queue_number(request):
    """Generate and print a new queue number without booking data"""
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
    
    return JsonResponse({
        'success': True,
        'number': next_number,
        'branch': branch.name,
        'date': today.strftime('%Y-%m-%d'),
        'time': timezone.now().strftime('%H:%M')
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
    if not request.user.can_inventory:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
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
    if not request.user.can_inventory:
        messages.error(request, "ليس لديك صلاحية الوصول")
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
                if not product_id:
                    return JsonResponse({'success': False, 'error': 'اختر صنفاً أولاً'})
                product = Product.objects.get(id=product_id, branch=branch)
                ok, msg = product.can_delete_catalog()
                if not ok:
                    return JsonResponse({'success': False, 'error': msg})
                product.delete()
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
                return JsonResponse({'success': True, 'message': 'تم تحديث الصنف'})

            if not code:
                code = Product.next_code(branch)
            elif Product.objects.filter(branch=branch, code=code).exists():
                return JsonResponse({'success': False, 'error': f'كود {code} موجود — اضغط Enter لتحميله'})

            Product.objects.create(
                branch=branch, code=code, name=name,
                price=0, cost=0, stock=0,
            )
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
    if not request.user.can_inventory:
        messages.error(request, "ليس لديك صلاحية الوصول")
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
    if not request.user.can_inventory:
        return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية'})
    branch = get_user_branch(request)
    qs = PurchaseInvoice.objects.filter(pk=pk)
    if branch:
        qs = qs.filter(branch=branch)
    purchase = get_object_or_404(qs)
    try:
        with transaction.atomic():
            purchase.reverse_stock()
            purchase.delete()
        return JsonResponse({
            'success': True,
            'message': 'تم حذف فاتورة المشتريات',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def inventory_consumption_add(request):
    """أصناف مستهلكة — تقليل المخزون."""
    if not request.user.can_inventory:
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
    if not request.user.can_inventory:
        return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية'})
    branch = get_user_branch(request)
    qs = ConsumptionInvoice.objects.filter(pk=pk)
    if branch:
        qs = qs.filter(branch=branch)
    consumption = get_object_or_404(qs)
    try:
        with transaction.atomic():
            consumption.reverse_stock()
            consumption.delete()
        return JsonResponse({'success': True, 'message': 'تم حذف حركة الاستهلاك'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def inventory_report(request):
    """تقرير المشتريات والاستهلاك."""
    if not request.user.can_inventory:
        return redirect('dashboard')

    branch = get_user_branch(request)
    ctx = _inventory_report_context(branch)
    ctx['branch'] = branch
    return render(request, 'salon/inventory_report.html', ctx)


@login_required
def inventory_report_pdf(request):
    if not request.user.can_inventory:
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
    if not request.user.can_inventory:
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
    if not request.user.can_inventory:
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
    if not request.user.can_inventory:
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

    return JsonResponse({
        'success': True,
        'message': msg,
        'serial_number': voucher.serial_number,
        'voucher_id': voucher.id,
        'next_serial': ExpenseVoucher.next_serial(branch, voucher_type),
    })


@login_required
def expense_list(request):
    if not request.user.can_expenses:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
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
    if not request.user.can_expenses:
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
                if not type_id:
                    return JsonResponse({'success': False, 'error': 'اختر مصروفاً أولاً'})
                expense_type = ExpenseType.objects.get(id=type_id, branch=branch)
                ok, msg = expense_type.can_delete_catalog()
                if not ok:
                    return JsonResponse({'success': False, 'error': msg})
                expense_type.delete()
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
                return JsonResponse({'success': True, 'message': 'تم تحديث المصروف'})

            if not code:
                code = ExpenseType.next_code(branch)
            elif ExpenseType.objects.filter(branch=branch, code=code).exists():
                return JsonResponse({'success': False, 'error': f'كود {code} موجود — اضغط Enter لتحميله'})

            ExpenseType.objects.create(branch=branch, code=code, name=name)
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
    if not request.user.can_expenses:
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
    if not request.user.can_expenses:
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
    banks = Bank.objects.filter(is_active=True)
    if branch:
        banks = banks.filter(Q(branch=branch) | Q(branch__isnull=True))
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
    if not request.user.can_expenses:
        return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية'})
    branch = get_user_branch(request)
    qs = ExpenseVoucher.objects.filter(pk=pk, voucher_type=voucher_type)
    if branch:
        qs = qs.filter(branch=branch)
    voucher = get_object_or_404(qs)
    voucher.delete()
    label = 'مرتد المصروف' if voucher_type == 'return' else 'المصروف'
    return JsonResponse({'success': True, 'message': f'تم حذف {label}'})


@login_required
def expense_add(request):
    return redirect('expense_out_add')

# =============================================================================
# reports_pdf
# =============================================================================


@login_required
def reports_pdf(request):
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

    barber_performance = invoices.values('barber__first_name', 'barber__last_name').annotate(
        total_sales=Sum('final_total'), invoice_count=Count('id')
    ).order_by('-total_sales')

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
        'barber_performance': barber_performance,
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

    # أداء الحلاقين
    barber_performance = invoices.values('barber__first_name', 'barber__last_name').annotate(
        total_sales=Sum('final_total'),
        invoice_count=Count('id')
    ).order_by('-total_sales')

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
        'barber_performance': barber_performance,
        'branch_stats': branch_stats,
        'total_cash_all': total_cash_all,        # 🔥
        'total_bank_all': total_bank_all,        # 🔥
        'grand_total_all': grand_total_all,      # 🔥
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'salon/reports.html', context)


# =============================================================================
# SERVICES
# =============================================================================

@login_required
def service_list(request):
    services = get_branch_queryset(request, Service, 'code')
    return render(request, 'salon/service_list.html', {'services': services})


@login_required
def service_add(request):
    """تكويد خدمة — مسلسل + اسم + سعر + نشط."""
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
                if not service_id:
                    return JsonResponse({'success': False, 'error': 'اختر خدمة أولاً'})
                service = Service.objects.get(id=service_id)
                ok, msg = service.can_delete_catalog()
                if not ok:
                    return JsonResponse({'success': False, 'error': msg})
                service.delete()
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
                return JsonResponse({'success': True, 'message': 'تم تحديث الخدمة'})

            if not code:
                code = Service.next_code()
            elif Service.objects.filter(code=code).exists():
                return JsonResponse({'success': False, 'error': f'مسلسل {code} موجود — اضغط Enter لتحميله'})

            Service.objects.create(
                code=code, name=name, price=price,
                is_active=is_active, cost=0, duration=30,
            )
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
    customers = get_branch_queryset(request, Customer)
    return render(request, 'salon/customer_list.html', {'customers': customers})


@login_required
def customer_add(request):
    branch = get_user_branch(request)

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.branch = branch or Branch.objects.first()
            customer.save()
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

    branches = Branch.objects.all() if request.user.is_superuser else Branch.objects.filter(id=get_user_branch(request).id) if get_user_branch(request) else Branch.objects.none()
    users = User.objects.all() if request.user.is_superuser else User.objects.filter(branch=get_user_branch(request))
    banks = Bank.objects.all() if request.user.is_superuser else Bank.objects.filter(branch=get_user_branch(request))

    return render(request, 'salon/settings.html', {
        'branches': branches,
        'users': users,
        'banks': banks,
    })


# =============================================================================
# USERS
# =============================================================================

# دالة مساعدة للتحقق من صلاحية المستخدم على إدارة المستخدمين وحماية الفروع
def check_user_permission(request, target_user=None):
    # إذا لم يكن سوبر يوزر وليس لديه صلاحية إدارة المستخدمين -> مرفوض
    if not request.user.is_superuser and not getattr(request.user, 'can_users', False):
        return False
    
    # حماية الفروع: لو مش سوبر يوزر وبيحاول يوصل لمستخدم في فرع تاني -> مرفوض
    if target_user and not request.user.is_superuser:
        user_branch = get_user_branch(request)
        if target_user.branch != user_branch:
            return False
            
    return True


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
    if not check_user_permission(request):
        messages.error(request, "⛔ ليس لديك صلاحية الوصول لإضافة مستخدمين")
        return redirect('dashboard')

    # تحديد الفروع المتاحة بناءً على الصلاحية
    if request.user.is_superuser:
        branches = Branch.objects.all()
    else:
        user_branch = get_user_branch(request)
        branches = Branch.objects.filter(id=user_branch.id) if user_branch else Branch.objects.none()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                
                # إجبار حيازة الفرع لو مش سوبر يوزر منعاً للتلاعب بالـ HTML
                if not request.user.is_superuser:
                    user.branch = get_user_branch(request)
                    
                password = form.cleaned_data.get('password')
                if password:
                    user.set_password(password)
                
                user.save()
                messages.success(request, f"✅ تم إنشاء المستخدم {user.username} بنجاح")
                return redirect('user_list') # تم التعديل ليوجه لقائمة اليوزرز بدلاً من سيتنج الكبيرة
            except Exception as e:
                messages.error(request, f"❌ خطأ أثناء الحفظ: {str(e)}")
        else:
            messages.error(request, f"❌ يرجى تصحيح الأخطاء: {form.errors}")
    else:
        form = UserForm()

    return render(request, 'salon/user_form.html', {
        'form': form,
        'branches': branches,
    })


@login_required
def user_edit(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    
    # التحقق من صلاحية التعديل على هذا المستخدم بالذات وفروعه
    if not check_user_permission(request, target_user=user_obj):
        messages.error(request, "⛔ غير مصرح لك بتعديل هذا المستخدم!")
        return redirect('user_list')

    # جلب الفروع هنا أيضاً (حل مشكلة عدم عمل الـ Edit بسبب حقل الفرع في التمبليت)
    if request.user.is_superuser:
        branches = Branch.objects.all()
    else:
        user_branch = get_user_branch(request)
        branches = Branch.objects.filter(id=user_branch.id) if user_branch else Branch.objects.none()

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_obj)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, f"✅ تم تعديل المستخدم {user.username} بنجاح")
            return redirect('user_list')
        else:
            messages.error(request, f"❌ خطأ في التعديل: {form.errors}")
    else:
        form = UserForm(instance=user_obj)

    return render(request, 'salon/user_form.html', {
        'form': form, 
        'user_obj': user_obj,
        'branches': branches # تم تمرير الفروع لضمان استقرار الفورم في التعديل
    })


@login_required
@require_POST
def user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    
    # التحقق من صلاحية الحذف على هذا المستخدم وفروعه
    if not check_user_permission(request, target_user=user_obj):
        messages.error(request, "⛔ غير مصرح لك بحذف هذا المستخدم!")
        return redirect('user_list')

    # منع المستخدم من ان يحذف حسابه الحالي الذي يعمل به
    if user_obj == request.user:
        messages.error(request, "❌ لا يمكنك حذف حسابك الحالي الذي تسجل به الدخول!")
        return redirect('user_list')
    
    username = user_obj.username
    user_obj.delete()
    messages.success(request, f"✅ تم حذف المستخدم {username} نهائياً")
    return redirect('user_list')

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

    banks = Bank.objects.filter(is_active=True)
    if not request.user.is_superuser:
        branch = get_user_branch(request)
        if branch:
            banks = banks.filter(branch=branch)

    return render(request, 'salon/bank_list.html', {'banks': banks})


@login_required
def bank_add(request):
    if not request.user.can_settings and not request.user.is_superuser:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    if request.user.is_superuser:
        branches = Branch.objects.all()
    else:
        user_branch = get_user_branch(request)
        branches = Branch.objects.filter(id=user_branch.id) if user_branch else Branch.objects.none()

    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            bank = form.save(commit=False)
            if not request.user.is_superuser:
                bank.branch = get_user_branch(request)
            bank.save()
            messages.success(request, "✅ تم إضافة البنك بنجاح")
            return redirect('settings')
    else:
        form = BankForm()
        if not request.user.is_superuser:
            form.fields['branch'].queryset = branches

    return render(request, 'salon/bank_form.html', {
        'form': form,
        'branches': branches,
    })


# =============================================================================
# PRINTING - Queue Tickets & Invoices
# =============================================================================

@login_required
def print_queue_ticket(request, pk):
    """Print a queue/waiting ticket"""
    booking = get_object_or_404(Booking, pk=pk)

    # Get services names
    services = [s.name for s in booking.services.all()]

    # Calculate estimated total
    estimated_total = sum(s.price for s in booking.services.all())

    context = {
        'queue_number': booking.queue_number,
        'customer_name': booking.customer_name,
        'barber_name': booking.barber.get_full_name() if booking.barber else '',
        'services': services,
        'estimated_total': estimated_total,
        'now': timezone.now(),
        'config': {
            'shop_name': getattr(settings, 'SALON_NAME', 'Salon Pro'),
            'shop_phone': getattr(settings, 'SALON_PHONE', ''),
            'shop_address': getattr(settings, 'SALON_ADDRESS', ''),
            'footer_text': 'شكراً لزيارتكم!',
        }
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
        'config': {
            'shop_name': getattr(settings, 'SALON_NAME', 'Salon Pro'),
            'shop_phone': getattr(settings, 'SALON_PHONE', ''),
            'shop_address': getattr(settings, 'SALON_ADDRESS', ''),
            'footer_text': 'شكراً لزيارتكم!',
        }
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
            barber_name=booking.barber.get_full_name() if booking.barber else '',
            services=services,
            estimated_total=estimated_total
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

        success, message = print_invoice_receipt(invoice, items)

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