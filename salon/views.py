"""
Salon Pro Views - Complete System
"""
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

from .models import (
    Branch, User, Category, Service, Product, Bank, Customer,
    Invoice, InvoiceItem, Booking, Expense, StockMovement
)
from .forms import (
    LoginForm, UserForm, BranchForm, CategoryForm, ServiceForm, ProductForm,
    BankForm, CustomerForm, BookingForm, ExpenseForm, StockMovementForm
)


# =============================================================================
# HELPERS
# =============================================================================

def get_user_branch(request):
    """Get branch for current user"""
    if request.user.is_superuser:
        return None  # Superuser sees all
    return request.user.branch


def get_branch_queryset(request, model, order_by='-created_at'):
    """Get queryset filtered by user branch"""
    branch = get_user_branch(request)
    if branch:
        return model.objects.filter(branch=branch).order_by(order_by)
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
    else:
        invoices_today = Invoice.objects.filter(created_at__date=today)
        expenses_today = Expense.objects.filter(date=today)
        waiting = Booking.objects.filter(status='waiting').count()
        low_stock = Product.objects.filter(stock__lte=F('min_stock')).count()

    revenue = invoices_today.aggregate(total=Sum('final_total'))['total'] or 0
    expenses = expenses_today.aggregate(total=Sum('amount'))['total'] or 0

    # Queue
    if branch:
        queue = Booking.objects.filter(branch=branch, status__in=['waiting', 'in_progress']).order_by('queue_number')[:10]
    else:
        queue = Booking.objects.filter(status__in=['waiting', 'in_progress']).order_by('queue_number')[:10]

    # Recent invoices
    recent = get_branch_queryset(request, Invoice)[:10]

    context = {
        'revenue': revenue,
        'expenses': expenses,
        'waiting': waiting,
        'low_stock': low_stock,
        'queue': queue,
        'recent_invoices': recent,
        'today': today,
    }
    return render(request, 'salon/dashboard.html', context)


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

    # Get services for POS (not products)
    # Get ALL services for POS (show everything, no filtering)
    if branch:
        services = Service.objects.filter(branch=branch)
        barbers = User.objects.filter(is_barber=True, branch=branch, is_active=True)
    else:
        services = Service.objects.all()
        barbers = User.objects.filter(is_barber=True, is_active=True)

    categories = Category.objects.filter(type='service', is_active=True)

    if request.method == 'POST':
        data = json.loads(request.body)
        items = data.get('items', [])

        if not items:
            return JsonResponse({'success': False, 'error': 'Cart is empty'})

        # Create invoice
        invoice = Invoice()
        invoice.branch = branch or Branch.objects.first()
        invoice.created_by = request.user

        # Customer
        customer_name = data.get('customer_name', '')
        customer_phone = data.get('customer_phone', '')
        if customer_name:
            customer, _ = Customer.objects.get_or_create(
                branch=invoice.branch, phone=customer_phone,
                defaults={'name': customer_name}
            )
            invoice.customer = customer

        # Barber
        barber_id = data.get('barber')
        if barber_id:
            invoice.barber = User.objects.get(id=barber_id)

        # Payment
        invoice.payment_method = data.get('payment_method', 'cash')
        bank_id = data.get('bank')
        if bank_id:
            invoice.bank = Bank.objects.get(id=bank_id)

        invoice.discount = Decimal(data.get('discount', 0))
        invoice.notes = data.get('notes', '')
        invoice.save()

        # Add items
        subtotal = 0
        for item in items:
            service = Service.objects.get(id=item['id'])
            InvoiceItem.objects.create(
                invoice=invoice,
                service=service,
                quantity=item['qty'],
                price=Decimal(item['price']),
                total=Decimal(item['qty']) * Decimal(item['price'])
            )
            subtotal += Decimal(item['qty']) * Decimal(item['price'])

        invoice.subtotal = subtotal
        invoice.save()

        # Update customer
        if invoice.customer:
            invoice.customer.visits_count += 1
            invoice.customer.total_spent += invoice.final_total
            invoice.customer.save()

        return JsonResponse({
            'success': True,
            'message': '✅ تم إتمام البيع بنجاح!',
            'invoice_id': invoice.id,
            'invoice_number': invoice.invoice_number
        })

    context = {
        'services': services,
        'categories': categories,
        'barbers': barbers,
    }
    return render(request, 'salon/pos.html', context)


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
    if not branch and not request.user.is_superuser:
        messages.error(request, "🏪 لم يتم تعيين فرع لهذا المستخدم")
        return redirect('dashboard')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.branch = branch or Branch.objects.first()

            # Generate queue number
            last = Booking.objects.filter(branch=booking.branch, created_at__date=timezone.now().date()).order_by('queue_number').last()
            booking.queue_number = (last.queue_number + 1) if last else 1

            booking.save()
            form.save_m2m()
            messages.success(request, f"✅ تم إضافة الحجز رقم {booking.queue_number} بنجاح")
            return redirect('booking_list')
    else:
        form = BookingForm()
        if branch:
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
# REPORTS
# =============================================================================

@login_required
def reports(request):
    if not request.user.can_reports:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    branch = get_user_branch(request)
    today = timezone.now().date()

    start_date = request.GET.get('start_date', today.replace(day=1))
    end_date = request.GET.get('end_date', today)

    # Base querysets
    if branch:
        invoices = Invoice.objects.filter(branch=branch, created_at__date__range=[start_date, end_date])
        expenses = Expense.objects.filter(branch=branch, date__range=[start_date, end_date])
    else:
        invoices = Invoice.objects.filter(created_at__date__range=[start_date, end_date])
        expenses = Expense.objects.filter(date__range=[start_date, end_date])

    # Summary
    total_revenue = invoices.aggregate(total=Sum('final_total'))['total'] or 0
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    net_profit = total_revenue - total_expenses
    total_invoices = invoices.count()

    # Payment breakdown
    payment_breakdown = invoices.values('payment_method', 'bank__name').annotate(
        total=Sum('final_total'), count=Count('id')
    )

    # Barber performance
    barber_performance = invoices.filter(barber__isnull=False).values(
        'barber__first_name', 'barber__last_name'
    ).annotate(
        total_sales=Sum('final_total'),
        invoice_count=Count('id')
    ).order_by('-total_sales')

    # Daily data
    daily_data = invoices.extra(select={'day': 'date(created_at)'}).values('day').annotate(
        total=Sum('final_total')
    ).order_by('day')

    # Banks for filter
    if branch:
        banks = Bank.objects.filter(branch=branch, is_active=True)
    else:
        banks = Bank.objects.filter(is_active=True)

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'total_invoices': total_invoices,
        'payment_breakdown': payment_breakdown,
        'barber_performance': barber_performance,
        'daily_data': list(daily_data),
        'banks': banks,
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
            service = form.save(commit=False)
            service.branch = branch or Branch.objects.first()
            service.save()
            messages.success(request, f"✅ تم إضافة الخدمة {service.name} بنجاح")
            return redirect('service_list')
    else:
        form = ServiceForm()
        form.fields['category'].queryset = Category.objects.filter(type='service', is_active=True)

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
        form.fields['category'].queryset = Category.objects.filter(type='product', is_active=True)

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
# SETTINGS - USERS, BRANCHES, CATEGORIES, BANKS
# =============================================================================

@login_required
def settings_view(request):
    if not request.user.can_settings and not request.user.is_superuser:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    return render(request, 'salon/settings.html')


# Users
@login_required
def user_list(request):
    if not request.user.can_users and not request.user.is_superuser:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    users = User.objects.all() if request.user.is_superuser else User.objects.filter(branch=get_user_branch(request))
    return render(request, 'salon/user_list.html', {'users': users})


@login_required
def user_add(request):
    if not request.user.can_users and not request.user.is_superuser:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, f"✅ تم إنشاء المستخدم {user.username} بنجاح")
            return redirect('user_list')
    else:
        form = UserForm()

    return render(request, 'salon/user_form.html', {'form': form})


# Branches
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


# Categories
@login_required
def category_list(request):
    if not request.user.can_settings and not request.user.is_superuser:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    categories = Category.objects.all()
    return render(request, 'salon/category_list.html', {'categories': categories})


@login_required
def category_add(request):
    if not request.user.can_settings and not request.user.is_superuser:
        messages.error(request, "⛔ ليس لديك صلاحية الوصول")
        return redirect('dashboard')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ تم إنشاء التصنيف بنجاح")
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'salon/category_form.html', {'form': form})


# Banks
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

    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ تم إضافة البنك بنجاح")
            return redirect('bank_list')
    else:
        form = BankForm()

    return render(request, 'salon/bank_form.html', {'form': form})


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