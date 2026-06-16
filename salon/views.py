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
    Invoice, InvoiceItem, Booking, Expense, StockMovement , DailyQueueNumber
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
        invoices_today = Invoice.objects.filter(branch=branch, created_at__date=today)
        expenses_today = Expense.objects.filter(branch=branch, date=today)
        waiting = Booking.objects.filter(branch=branch, status='waiting').count()
        low_stock = Product.objects.filter(branch=branch, stock__lte=F('min_stock')).count()
        # <-- هنا المشكلة: لازم يكون queue مش bookings
        queue = Booking.objects.filter(branch=branch, status__in=['waiting', 'in_progress']).order_by('queue_number')[:10]
    else:
        invoices_today = Invoice.objects.filter(created_at__date=today)
        expenses_today = Expense.objects.filter(date=today)
        waiting = Booking.objects.filter(status='waiting').count()
        low_stock = Product.objects.filter(stock__lte=F('min_stock')).count()
        queue = Booking.objects.filter(status__in=['waiting', 'in_progress']).order_by('queue_number')[:10]

    revenue = invoices_today.aggregate(total=Sum('final_total'))['total'] or 0
    expenses = expenses_today.aggregate(total=Sum('amount'))['total'] or 0

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

@csrf_protect
def send_whatsapp_invoice(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone = data.get('phone', '').replace(" ", "")
            invoice_number = data.get('invoice_number', '')
            invoice_id = data.get('invoice_id', '')

            api_key = getattr(settings, "WHATSAPP_API_KEY", None)
            api_url = getattr(settings, "WHATSAPP_API_URL", None)
            
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
        invoice_id = data.get('invoice_id')  # جلب معرف الفاتورة إن وجد (حالة التعديل)

        if not items:
            return JsonResponse({'success': False, 'error': 'السلة فارغة!'})

        try:
            # استخدام atomic لمنع مشاكل الـ Race Condition وتداخل طلبات الـ Multi-user
            with transaction.atomic():
                if invoice_id:
                    # حالة التعديل: جلب الفاتورة وعمل قفل عليها في الداتابيز لحين انتهاء المعاملة
                    invoice = Invoice.objects.select_for_update().get(id=invoice_id)
                    
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
                    if not invoice_id:  # زيادة عدد الزيارات فقط لو كانت فاتورة جديدة وليست تعديلاً
                        invoice.customer.visits_count += 1
                    invoice.customer.total_spent += invoice.final_total
                    invoice.customer.save()

            return JsonResponse({
                'success': True,
                'message': '✅ تم الحفظ بنجاح!',
                'invoice_id': invoice.id,
                'invoice_number': invoice.invoice_number
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
    """
    دالة مخصصة لجلب بيانات فاتورة قديمة بصيغة JSON 
    وعرض محتوياتها داخل شاشة الـ POS لإعادة التعديل عليها
    """
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        items_data = []
        
        for item in invoice.items.all():
            items_data.append({
                'id': item.service.id if item.service else None,
                'name': item.service.name if item.service else (item.product.name if item.product else "خدمة غير معروفة"),
                'price': str(item.price),
                'qty': item.quantity,
            })
            
        return JsonResponse({
            'success': True,
            'invoice': {
                'id': invoice.id,
                'invoice_number': invoice.invoice_number,
                'customer_name': invoice.customer.name if invoice.customer else '',
                'customer_phone': invoice.customer.phone if invoice.customer else '',
                'barber_id': invoice.barber.id if invoice.barber else '',
                'payment_method': invoice.payment_method,
                'bank_id': invoice.bank.id if invoice.bank else '',
                'discount': str(invoice.discount),
                'items': items_data
            }
        })
    except Invoice.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'الفاتورة المطلوبة غير موجودة.'})
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
    branch = get_user_branch(request)
    
    # تأكد إن فيه فرع
    if not branch:
        branch = Branch.objects.filter(is_active=True).first()
    
    if not branch:
        messages.error(request, "❌ لا يوجد فرع نشط! الرجاء إنشاء فرع أولاً.")
        return redirect('branch_add')  # أو redirect('dashboard')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.branch = branch  # <-- دلوقتي مضمون إنه مش None

            # Generate queue number
            today = timezone.now().date()
            tomorrow = today + timezone.timedelta(days=1)
            
            last = Booking.objects.filter(
                branch=booking.branch,
                created_at__gte=today,
                created_at__lt=tomorrow
            ).order_by('queue_number').last()
            
            booking.queue_number = (last.queue_number + 1) if last else 1

            booking.save()
            form.save_m2m()
            messages.success(request, f"✅ تم إضافة الحجز رقم {booking.queue_number} بنجاح")
            return redirect('booking_list')
    else:
        form = BookingForm()
        form.fields['barber'].queryset = User.objects.filter(is_barber=True, branch=branch)

    return render(request, 'salon/booking_form.html', {'form': form})

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

@login_required
def expense_list(request):
    if not request.user.can_expenses:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    expenses = get_branch_queryset(request, Expense, '-date')
    return render(request, 'salon/expense_list.html', {'expenses': expenses})


@login_required
def expense_add(request):
    if not request.user.can_expenses:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    branch = get_user_branch(request)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.branch = branch or Branch.objects.first()
            expense.created_by = request.user
            expense.save()
            messages.success(request, "✅ تم تسجيل المصروف بنجاح")
            return redirect('expense_list')
    else:
        form = ExpenseForm()

    return render(request, 'salon/expense_form.html', {'form': form})

# =============================================================================
# reports_pdf
# =============================================================================


@login_required
def reports_pdf(request):
    branch = get_user_branch(request)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    invoices = Invoice.objects.all()
    expenses = Expense.objects.all()
    
    if not request.user.is_superuser:
        if not branch:
            messages.error(request, "🏪 لم يتم تعيين فرع لهذا المستخدم")
            return redirect('dashboard')
        invoices = invoices.filter(branch=branch)
        expenses = expenses.filter(branch=branch)
    
    if start_date and end_date:
        invoices = invoices.filter(created_at__date__range=[start_date, end_date])
        expenses = expenses.filter(date__range=[start_date, end_date])
    
    total_revenue = invoices.aggregate(total=Sum('final_total'))['total'] or 0
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
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
    expenses = Expense.objects.all()
    
    if not request.user.is_superuser:
        if not branch:
            messages.error(request, "🏪 لم يتم تعيين فرع لهذا المستخدم")
            return redirect('dashboard')
        invoices = invoices.filter(branch=branch)
        expenses = expenses.filter(branch=branch)
    
    if start_date and end_date:
        invoices = invoices.filter(created_at__date__range=[start_date, end_date])
        expenses = expenses.filter(date__range=[start_date, end_date])
    
    # التوتال العام
    total_revenue = invoices.aggregate(total=Sum('final_total'))['total'] or 0
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
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
    services = get_branch_queryset(request, Service, 'name')
    return render(request, 'salon/service_list.html', {'services': services})


@login_required
def service_add(request):
    branch = get_user_branch(request)

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            # service.branch = branch or Branch.objects.first()
            service.save()
            messages.success(request, f"✅ تم إضافة الخدمة {service.name} بنجاح")
            return redirect('service_list')
    else:
        form = ServiceForm()

    return render(request, 'salon/service_form.html', {'form': form})


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