"""
Salon Pro - Complete Accounting & Management System
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


# =============================================================================
# BRANCHES
# =============================================================================

class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name="Branch Name")
    address = models.TextField(blank=True, verbose_name="Address")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    is_main = models.BooleanField(default=False, verbose_name="Main Branch (Admin)")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
        ordering = ['-is_main', 'name']

    def __str__(self):
        return f"{'🏢 ' if self.is_main else '🏪 '}{self.name}"


class SalonSettings(models.Model):
    """إعدادات الصالون العامة — للطباعة والعرض في الإعدادات."""
    salon_name = models.CharField(max_length=100, default='صالون برو', verbose_name="اسم الصالون")
    phone = models.CharField(max_length=20, blank=True, verbose_name="الهاتف")
    address = models.TextField(blank=True, verbose_name="العنوان")
    logo = models.ImageField(upload_to='salon/logo/', blank=True, verbose_name="الشعار")
    currency = models.CharField(max_length=10, default='EGP', verbose_name="العملة")
    receipt_size = models.CharField(max_length=10, default='80mm', verbose_name="نمط الطباعة")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="الضريبة %")
    auto_backup = models.BooleanField(default=False, verbose_name="نسخ احتياطي")
    sms_notifications = models.BooleanField(default=False, verbose_name="SMS")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Salon Settings"
        verbose_name_plural = "Salon Settings"

    def __str__(self):
        return self.salon_name

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def print_config(self, request=None):
        logo_url = ''
        if self.logo:
            logo_url = self.logo.url
            if request:
                logo_url = request.build_absolute_uri(self.logo.url)
        return {
            'shop_name': self.salon_name or 'صالون برو',
            'shop_phone': self.phone or '',
            'shop_address': self.address or '',
            'shop_logo': logo_url,
            'footer_text': 'شكراً لزيارتكم!',
        }


# =============================================================================
# USERS & PERMISSIONS
# =============================================================================

class User(AbstractUser):
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='users', verbose_name="Branch"
    )
    user_code = models.CharField(max_length=20, blank=True, unique=True, verbose_name="كود المستخدم")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    photo = models.ImageField(upload_to='users/', blank=True, verbose_name="Photo")
    is_barber = models.BooleanField(default=False, verbose_name="Is Barber")
    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, null=True, blank=True,
        verbose_name="Commission %"
    )

    # Permissions — الكل false افتراضياً للمستخدمين الجدد
    can_pos = models.BooleanField(default=False, verbose_name="Can Access POS")
    can_inventory = models.BooleanField(default=False, verbose_name="Can Access Inventory")
    can_expenses = models.BooleanField(default=False, verbose_name="Can Access Expenses")
    can_reports = models.BooleanField(default=False, verbose_name="Can Access Reports")
    can_settings = models.BooleanField(default=False, verbose_name="Can Access Settings")
    can_users = models.BooleanField(default=False, verbose_name="Can Manage Users")
    can_audit = models.BooleanField(default=False, verbose_name="Can Access Audit")
    can_bookings = models.BooleanField(default=False, verbose_name="Can Access Bookings")
    can_customers = models.BooleanField(default=False, verbose_name="Can Access Customers")
    can_services = models.BooleanField(default=False, verbose_name="Can Access Services")
    can_employees = models.BooleanField(default=False, verbose_name="Can Access Employees")
    can_delete_pos = models.BooleanField(default=False, verbose_name="Can Delete POS")
    can_delete_bookings = models.BooleanField(default=False, verbose_name="Can Delete Bookings")
    can_delete_expenses = models.BooleanField(default=False, verbose_name="Can Delete Expenses")
    can_delete_inventory = models.BooleanField(default=False, verbose_name="Can Delete Inventory")
    can_delete_employees = models.BooleanField(default=False, verbose_name="Can Delete Employees")
    can_delete_services = models.BooleanField(default=False, verbose_name="Can Delete Services")

    # Sub-permissions — expenses
    can_expense_types = models.BooleanField(default=False, verbose_name="Expense Types")
    can_expense_out = models.BooleanField(default=False, verbose_name="Expense Out")
    can_expense_return = models.BooleanField(default=False, verbose_name="Expense Return")

    # Sub-permissions — inventory
    can_inv_items = models.BooleanField(default=False, verbose_name="Inventory Items")
    can_inv_purchase = models.BooleanField(default=False, verbose_name="Inventory Purchase")
    can_inv_consumption = models.BooleanField(default=False, verbose_name="Inventory Consumption")
    can_inv_report = models.BooleanField(default=False, verbose_name="Inventory Report")
    can_inv_totals = models.BooleanField(default=False, verbose_name="Inventory Totals")

    # Sub-permissions — reports
    can_report_activity = models.BooleanField(default=False, verbose_name="Activity Log")
    can_report_statement = models.BooleanField(default=False, verbose_name="Account Statement")

    # Sub-permissions — bookings
    can_booking_vip = models.BooleanField(default=False, verbose_name="VIP Booking")
    can_booking_queue = models.BooleanField(default=False, verbose_name="Queue Number")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.branch})"

    @property
    def is_admin(self):
        if self.is_superuser:
            return True
        if self.branch and self.branch.is_main:
            return True
        return False

    @property
    def can_see_all_branches(self):
        return self.is_superuser or (self.branch and self.branch.is_main)

    @classmethod
    def next_code(cls):
        nums = []
        for code in cls.objects.values_list('user_code', flat=True):
            if str(code).isdigit():
                nums.append(int(code))
        return str(max(nums) + 1) if nums else '1'

    def can_delete_account(self):
        if self.is_superuser:
            return False, 'لا يمكن حذف مدير النظام'
        checks = [
            (self.created_invoices.exists(), 'فواتير مبيعات'),
            (self.invoices.exists(), 'فواتير كحلاق'),
            (self.bookings.exists(), 'حجوزات'),
            (self.purchase_invoices.exists(), 'مشتريات مخزن'),
            (self.consumption_invoices.exists(), 'استهلاك مخزن'),
            (self.expense_vouchers.exists(), 'سندات مصروفات'),
            (self.created_expenses.exists(), 'مصروفات قديمة'),
            (self.stock_movements.exists(), 'حركات مخزون'),
        ]
        linked = [label for ok, label in checks if ok]
        if linked:
            return False, 'مربوط بـ: ' + '، '.join(linked)
        return True, ''


# =============================================================================
# CATEGORIES - Optional now
# =============================================================================

class Category(models.Model):
    TYPE_CHOICES = [
        ('service', 'Service'),
        ('product', 'Product'),
        ('expense', 'Expense Category'),
    ]
    name = models.CharField(max_length=50, verbose_name="Name")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='service', verbose_name="Type")
    icon = models.CharField(max_length=30, default="✂️", verbose_name="Icon")
    color = models.CharField(max_length=7, default="#6c5ce7", verbose_name="Color")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['type', 'name']

    def __str__(self):
        return f"{self.icon} {self.name} ({self.get_type_display()})"


# =============================================================================
# SERVICES
# =============================================================================

class Service(models.Model):
    # branch = models.ForeignKey(
    #     Branch, on_delete=models.CASCADE, related_name='services',
    #     verbose_name="Branch"
    # )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='services', limit_choices_to={'type': 'service'},
        verbose_name="Category"
    )
    name = models.CharField(max_length=100, verbose_name="Service Name")
    code = models.CharField(max_length=20, blank=True, verbose_name="Code")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Cost")
    duration = models.PositiveIntegerField(default=30, verbose_name="Duration (minutes)")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.price} EGP"

    @classmethod
    def next_code(cls):
        nums = []
        for code in cls.objects.values_list('code', flat=True):
            if str(code).isdigit():
                nums.append(int(code))
        return str(max(nums) + 1) if nums else '1'

    def can_delete_catalog(self):
        if self.invoice_items.exists():
            return False, 'لا يمكن الحذف — الخدمة مربوطة بمبيعات'
        if self.booking_set.exists():
            return False, 'لا يمكن الحذف — الخدمة مربوطة بحجوزات'
        return True, ''


# =============================================================================
# PRODUCTS
# =============================================================================

class Product(models.Model):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='products',
        verbose_name="Branch"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='products', limit_choices_to={'type': 'product'},
        verbose_name="Category"
    )
    name = models.CharField(max_length=100, verbose_name="Product Name")
    code = models.CharField(max_length=20, blank=True, verbose_name="Code")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sale Price")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Cost Price")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    min_stock = models.PositiveIntegerField(default=5, verbose_name="Min Stock Alert")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - Stock: {self.stock} - {self.price} EGP"

    @property
    def is_low_stock(self):
        return self.stock <= self.min_stock

    @classmethod
    def next_code(cls, branch):
        nums = []
        for code in cls.objects.filter(branch=branch).values_list('code', flat=True):
            if str(code).isdigit():
                nums.append(int(code))
        return str(max(nums) + 1) if nums else '1'

    def can_delete_catalog(self):
        if self.stock > 0:
            return False, 'لا يمكن الحذف — الصنف له كمية في المخزون'
        if self.purchase_items.exists():
            return False, 'لا يمكن الحذف — الصنف مربوط بفواتير مشتريات'
        if self.invoice_items.exists():
            return False, 'لا يمكن الحذف — الصنف مربوط بمبيعات'
        if self.movements.exists():
            return False, 'لا يمكن الحذف — الصنف له حركات مخزون'
        return True, ''


# =============================================================================
# PURCHASE INVOICES (مشتريات المخزن)
# =============================================================================

class PurchaseInvoice(models.Model):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='purchase_invoices',
        verbose_name="Branch",
    )
    serial_number = models.PositiveIntegerField(default=0, verbose_name="المسلسل")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='purchase_invoices', verbose_name="Created By",
    )

    class Meta:
        verbose_name = "Purchase Invoice"
        verbose_name_plural = "Purchase Invoices"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'serial_number'],
                name='unique_branch_purchase_serial',
            ),
        ]

    def __str__(self):
        return f"مشتريات #{self.serial_number}"

    @classmethod
    def next_serial(cls, branch):
        from django.db.models import Max
        last = cls.objects.filter(branch=branch).aggregate(m=Max('serial_number'))['m'] or 0
        return last + 1

    def save(self, *args, **kwargs):
        if self.branch_id and not self.serial_number:
            self.serial_number = PurchaseInvoice.next_serial(self.branch)
        super().save(*args, **kwargs)

    @property
    def total_cost(self):
        return sum(i.line_cost for i in self.items.all())

    @property
    def total_price(self):
        return sum(i.line_price for i in self.items.all())

    def reverse_stock(self):
        """عكس تأثير الفاتورة على المخزون."""
        for item in self.items.select_related('product'):
            p = item.product
            p.stock = max(0, int(p.stock) - int(item.quantity))
            p.save(update_fields=['stock'])
        StockMovement.objects.filter(reference_invoice=self).delete()
        self.items.all().delete()


class PurchaseInvoiceItem(models.Model):
    purchase = models.ForeignKey(
        PurchaseInvoice, on_delete=models.CASCADE, related_name='items',
        verbose_name="Purchase",
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='purchase_items',
        verbose_name="Product",
    )
    quantity = models.PositiveIntegerField(verbose_name="Qty")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Cost")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")

    class Meta:
        verbose_name = "Purchase Item"
        verbose_name_plural = "Purchase Items"

    @property
    def line_cost(self):
        return self.quantity * self.cost

    @property
    def line_price(self):
        return self.quantity * self.price


# =============================================================================
# CONSUMPTION INVOICES (أصناف مستهلكة)
# =============================================================================

class ConsumptionInvoice(models.Model):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='consumption_invoices',
        verbose_name="Branch",
    )
    serial_number = models.PositiveIntegerField(default=0, verbose_name="المسلسل")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='consumption_invoices', verbose_name="Created By",
    )

    class Meta:
        verbose_name = "Consumption Invoice"
        verbose_name_plural = "Consumption Invoices"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'serial_number'],
                name='unique_branch_consumption_serial',
            ),
        ]

    def __str__(self):
        return f"استهلاك #{self.serial_number}"

    @classmethod
    def next_serial(cls, branch):
        from django.db.models import Max
        last = cls.objects.filter(branch=branch).aggregate(m=Max('serial_number'))['m'] or 0
        return last + 1

    def save(self, *args, **kwargs):
        if self.branch_id and not self.serial_number:
            self.serial_number = ConsumptionInvoice.next_serial(self.branch)
        super().save(*args, **kwargs)

    def reverse_stock(self):
        for item in self.items.select_related('product'):
            item.product.stock += item.quantity
            item.product.save(update_fields=['stock'])
        StockMovement.objects.filter(reference_consumption=self).delete()
        self.items.all().delete()


class ConsumptionInvoiceItem(models.Model):
    consumption = models.ForeignKey(
        ConsumptionInvoice, on_delete=models.CASCADE, related_name='items',
        verbose_name="Consumption",
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='consumption_items',
        verbose_name="Product",
    )
    quantity = models.PositiveIntegerField(verbose_name="Qty")
    unit_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Unit Cost",
    )

    class Meta:
        verbose_name = "Consumption Item"
        verbose_name_plural = "Consumption Items"

    @property
    def line_cost(self):
        return self.quantity * self.unit_cost


# =============================================================================
# BANKS
# =============================================================================

class Bank(models.Model):
    name = models.CharField(max_length=100, verbose_name="Bank Name")
    account_number = models.CharField(max_length=50, blank=True, verbose_name="Account Number")
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='banks',
        verbose_name="Branch", null=True, blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"
        ordering = ['name']

    def __str__(self):
        return self.name


# =============================================================================
# CUSTOMERS
# =============================================================================

class Customer(models.Model):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='customers',
        verbose_name="Branch"
    )
    name = models.CharField(max_length=100, verbose_name="Name")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    email = models.EmailField(blank=True, verbose_name="Email")
    notes = models.TextField(blank=True, verbose_name="Notes")
    visits_count = models.PositiveIntegerField(default=0, verbose_name="Visits")
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total Spent")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.phone}"


# =============================================================================
# EMPLOYEES
# =============================================================================

class Employee(models.Model):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='employees',
        verbose_name="Branch",
    )
    serial_number = models.CharField(max_length=30, verbose_name="كود الموظف")
    name = models.CharField(max_length=100, verbose_name="اسم الموظف")
    phone = models.CharField(max_length=20, blank=True, default='', verbose_name="Phone")
    job_title = models.CharField(max_length=50, blank=True, default='', verbose_name="الوظيفة")
    base_salary = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="الراتب",
    )
    hire_date = models.DateField(verbose_name="تاريخ التعيين")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    notes = models.TextField(blank=True, default='', verbose_name="Notes")
    daily_number = models.PositiveIntegerField(default=0, verbose_name="رقم يومي")
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='employee_profile', verbose_name="User",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'salon_employee'
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ['serial_number']
        unique_together = [('branch', 'serial_number')]

    def __str__(self):
        return f"{self.serial_number} - {self.name}"

    @classmethod
    def next_code(cls, branch):
        nums = []
        for sn in cls.objects.filter(branch=branch).values_list('serial_number', flat=True):
            if str(sn).isdigit():
                nums.append(int(sn))
        return str(max(nums) + 1) if nums else '1'

    def can_delete_catalog(self):
        if self.invoices.exists():
            return False, 'لا يمكن الحذف — الموظف مربوط بفواتير'
        if self.bookings.exists():
            return False, 'لا يمكن الحذف — الموظف مربوط بحجوزات'
        return True, ''


# =============================================================================
# INVOICES & POS
# =============================================================================

class Invoice(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('visa', 'Visa'),
        ('bank', 'Bank Transfer'),
    ]

    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='invoices',
        verbose_name="Branch"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='invoices', verbose_name="Customer"
    )
    barber = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='invoices', verbose_name="Barber"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='invoices', verbose_name="Employee",
    )
    invoice_number = models.CharField(max_length=20, verbose_name="رقم الفاتورة")
    serial_number = models.PositiveIntegerField(
        default=0, verbose_name="المسلسل",
    )
    daily_number = models.PositiveIntegerField(
        default=0, verbose_name="المسلسل اليومي",
    )
    document_date = models.DateField(
        null=True, blank=True, verbose_name="تاريخ المستند",
    )
    is_voided = models.BooleanField(default=False, verbose_name="ملغاة")

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Subtotal")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Discount")
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Tax")
    final_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Final Total")

    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHODS, default='cash',
        verbose_name="Payment Method"
    )
    bank = models.ForeignKey(
        Bank, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='invoices', verbose_name="Bank"
    )
    booking = models.ForeignKey(
        'Booking', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='invoices', verbose_name="Booking",
    )

    notes = models.TextField(blank=True, verbose_name="Notes")
    is_paid = models.BooleanField(default=True, verbose_name="Paid")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='created_invoices', verbose_name="Created By"
    )

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'serial_number'],
                name='unique_branch_invoice_serial',
            ),
        ]

    def __str__(self):
        return f"#{self.display_number()} - {self.final_total} EGP"

    def display_number(self):
        return self.serial_number or self.invoice_number

    def can_edit_today(self):
        if not self.created_at:
            return False
        return timezone.localtime(self.created_at).date() == timezone.localdate()

    @classmethod
    def next_serial(cls, branch):
        from django.db.models import Max
        last = cls.objects.filter(branch=branch, is_voided=False).aggregate(
            m=Max('serial_number'),
        )['m'] or 0
        # المسلسل لا يُعاد — حتى الفواتير الملغاة تحتفظ برقمها والتالي يكمل
        last_all = cls.objects.filter(branch=branch).aggregate(m=Max('serial_number'))['m'] or 0
        return last_all + 1

    def save(self, *args, **kwargs):
        if self.branch_id and not self.serial_number:
            self.serial_number = Invoice.next_serial(self.branch)
        if not self.invoice_number:
            self.invoice_number = str(self.serial_number)
        self.daily_number = self.serial_number
        if not self.document_date:
            self.document_date = timezone.localdate()
        self.final_total = self.subtotal - self.discount + self.tax
        super().save(*args, **kwargs)

    def generate_invoice_number(self):
        """Legacy — لم يعد يُستخدم."""
        return str(self.serial_number or '')


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='items',
        verbose_name="Invoice"
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=True, blank=True,
        related_name='invoice_items', verbose_name="Service"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True,
        related_name='invoice_items', verbose_name="Product"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Qty")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total")

    class Meta:
        verbose_name = "Invoice Item"
        verbose_name_plural = "Invoice Items"

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

        # Update product stock
        if self.product:
            self.product.stock -= self.quantity
            self.product.save()


# =============================================================================
# DailyQueueNumber
# =============================================================================

class DailyQueueNumber(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='daily_numbers')
    date = models.DateField(default=timezone.now)
    last_number = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['branch', 'date']
        verbose_name = "رقم الدور اليومي"
        verbose_name_plural = "أرقام الدور اليومية"
    
    def __str__(self):
        return f"{self.branch} - {self.date} - #{self.last_number}"
    
    def get_next_number(self):
        self.last_number += 1
        self.save()
        return self.last_number

# =============================================================================
# BOOKINGS
# =============================================================================

class Booking(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='bookings',
        verbose_name="Branch"
    )
    customer_name = models.CharField(max_length=100, verbose_name="Customer Name")
    customer_phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    services = models.ManyToManyField(Service, blank=True, verbose_name="Services")
    barber = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='bookings', verbose_name="Barber"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='bookings', verbose_name="Employee",
    )
    queue_number = models.PositiveIntegerField(verbose_name="Queue #")
    serial_number = models.PositiveIntegerField(
        default=0, verbose_name="المسلسل",
    )
    daily_number = models.PositiveIntegerField(
        default=0, verbose_name="رقم يومي",
    )
    is_vip = models.BooleanField(default=False, verbose_name="حجز VIP")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='waiting',
        verbose_name="Status"
    )
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Started")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Completed")

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['queue_number', 'created_at']

    def __str__(self):
        return f"#{self.queue_number} - {self.customer_name}"

    def save(self, *args, **kwargs):
        if not self.serial_number:
            if self.queue_number:
                self.serial_number = self.queue_number
            elif self.branch_id:
                from django.db.models import Max
                last = Booking.objects.filter(branch=self.branch).aggregate(
                    m=Max('serial_number'),
                )['m'] or 0
                self.serial_number = last + 1
        if not self.daily_number:
            self.daily_number = self.queue_number or self.serial_number
        super().save(*args, **kwargs)


# =============================================================================
# EXPENSES
# =============================================================================

class Expense(models.Model):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='expenses',
        verbose_name="Branch"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='expenses', limit_choices_to={'type': 'expense'},
        verbose_name="Category"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Amount")
    description = models.TextField(verbose_name="Description")
    date = models.DateField(default=timezone.now, verbose_name="Date")
    receipt = models.ImageField(upload_to='receipts/', blank=True, verbose_name="Receipt")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='created_expenses', verbose_name="Created By"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.category} - {self.amount} EGP"


class ExpenseType(models.Model):
    """تكويد أنواع المصروفات — كود + اسم."""
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='expense_types',
        verbose_name="Branch",
    )
    code = models.CharField(max_length=20, blank=True, verbose_name="Code")
    name = models.CharField(max_length=100, verbose_name="اسم المصروف")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Expense Type"
        verbose_name_plural = "Expense Types"
        ordering = ['code', 'name']

    def __str__(self):
        return f"{self.code} — {self.name}" if self.code else self.name

    @classmethod
    def next_code(cls, branch):
        nums = []
        for code in cls.objects.filter(branch=branch).values_list('code', flat=True):
            if str(code).isdigit():
                nums.append(int(code))
        return str(max(nums) + 1) if nums else '1'

    def can_delete_catalog(self):
        if self.vouchers.exists():
            return False, 'لا يمكن الحذف — المصروف مربوط بحركات'
        return True, ''


class ExpenseVoucher(models.Model):
    """سند مصروف أو مرتد مصروف."""
    VOUCHER_TYPES = [
        ('out', 'مصروف'),
        ('return', 'مرتد'),
    ]
    PAYMENT_METHODS = [
        ('cash', 'كاش'),
        ('bank', 'بنك'),
    ]

    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='expense_vouchers',
        verbose_name="Branch",
    )
    voucher_type = models.CharField(
        max_length=10, choices=VOUCHER_TYPES, default='out',
        verbose_name="نوع السند",
    )
    serial_number = models.PositiveIntegerField(default=0, verbose_name="المسلسل")
    expense_type = models.ForeignKey(
        ExpenseType, on_delete=models.PROTECT, related_name='vouchers',
        verbose_name="المصروف",
    )
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHODS, default='cash',
        verbose_name="طريقة الدفع",
    )
    bank = models.ForeignKey(
        Bank, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='expense_vouchers', verbose_name="البنك",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="المبلغ")
    date = models.DateField(default=timezone.now, verbose_name="التاريخ")
    notes = models.TextField(blank=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='expense_vouchers', verbose_name="Created By",
    )

    class Meta:
        verbose_name = "Expense Voucher"
        verbose_name_plural = "Expense Vouchers"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'voucher_type', 'serial_number'],
                name='unique_branch_expense_voucher_serial',
            ),
        ]

    def __str__(self):
        label = 'مرتد' if self.voucher_type == 'return' else 'مصروف'
        return f"{label} #{self.serial_number} — {self.expense_type} — {self.amount}"

    @classmethod
    def next_serial(cls, branch, voucher_type='out'):
        from django.db.models import Max
        last = cls.objects.filter(
            branch=branch, voucher_type=voucher_type,
        ).aggregate(m=Max('serial_number'))['m'] or 0
        return last + 1

    def save(self, *args, **kwargs):
        if self.branch_id and not self.serial_number:
            self.serial_number = ExpenseVoucher.next_serial(self.branch, self.voucher_type)
        super().save(*args, **kwargs)


# =============================================================================
# STOCK MOVEMENTS
# =============================================================================

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjust', 'Adjustment'),
    ]

    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='stock_movements',
        verbose_name="Branch"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='movements',
        verbose_name="Product"
    )
    movement_type = models.CharField(
        max_length=10, choices=MOVEMENT_TYPES, verbose_name="Type"
    )
    quantity = models.IntegerField(verbose_name="Quantity")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Cost")
    notes = models.TextField(blank=True, verbose_name="Notes")
    date = models.DateField(default=timezone.now, verbose_name="Date")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='stock_movements', verbose_name="Created By"
    )
    serial_number = models.PositiveIntegerField(default=0, verbose_name="المسلسل")
    daily_number = models.PositiveIntegerField(default=0, verbose_name="رقم يومي")
    reference_invoice = models.ForeignKey(
        PurchaseInvoice, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='movements', verbose_name="فاتورة مشتريات",
        db_column='reference_invoice_id',
    )
    reference_consumption = models.ForeignKey(
        'ConsumptionInvoice', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='movements', verbose_name="فاتورة استهلاك",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product} - {self.get_movement_type_display()} {self.quantity}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if self.reference_invoice_id and not self.serial_number:
            self.serial_number = self.reference_invoice.serial_number
        if self.reference_consumption_id and not self.serial_number:
            self.serial_number = self.reference_consumption.serial_number
        if not self.serial_number and self.branch_id:
            from django.db.models import Max
            last = StockMovement.objects.filter(branch=self.branch).aggregate(
                m=Max('serial_number'),
            )['m'] or 0
            self.serial_number = last + 1
        if not self.daily_number:
            self.daily_number = self.serial_number or 1
        super().save(*args, **kwargs)
        if is_new:
            if self.movement_type == 'in':
                self.product.stock += self.quantity
            elif self.movement_type == 'out':
                self.product.stock -= self.quantity
            self.product.save()


# =============================================================================
# ACTIVITY LOG (سجل الحركات)
# =============================================================================

class ActivityLog(models.Model):
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_VOID = 'void'

    ACTION_CHOICES = [
        (ACTION_CREATE, 'إنشاء'),
        (ACTION_UPDATE, 'تعديل'),
        (ACTION_DELETE, 'حذف'),
        (ACTION_VOID, 'إلغاء'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='activity_logs', verbose_name='المستخدم',
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='activity_logs', verbose_name='الفرع',
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, verbose_name='العملية')
    entity_type = models.CharField(max_length=50, verbose_name='النوع')
    entity_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='المعرف')
    entity_label = models.CharField(max_length=255, verbose_name='الوصف')
    details = models.TextField(blank=True, default='', verbose_name='تفاصيل')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='الوقت')

    class Meta:
        verbose_name = 'سجل حركة'
        verbose_name_plural = 'سجل الحركات'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_action_display()} — {self.entity_type}: {self.entity_label}'

    @property
    def action_badge_class(self):
        return {
            self.ACTION_CREATE: 'success',
            self.ACTION_UPDATE: 'primary',
            self.ACTION_DELETE: 'danger',
            self.ACTION_VOID: 'warning',
        }.get(self.action, 'secondary')


# =============================================================================
# ACCOUNT TRANSFERS (تحويل بين نقدية وبنوك)
# =============================================================================

class AccountTransfer(models.Model):
    DIRECTION_CASH_TO_BANK = 'cash_to_bank'
    DIRECTION_BANK_TO_CASH = 'bank_to_cash'
    DIRECTION_CHOICES = [
        (DIRECTION_CASH_TO_BANK, 'نقدية → بنك'),
        (DIRECTION_BANK_TO_CASH, 'بنك → نقدية'),
    ]

    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='account_transfers',
        verbose_name='الفرع',
    )
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES, verbose_name='الاتجاه')
    bank = models.ForeignKey(
        Bank, on_delete=models.PROTECT, related_name='account_transfers',
        verbose_name='البنك',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='المبلغ')
    notes = models.TextField(blank=True, default='', verbose_name='بيان')
    date = models.DateField(default=timezone.now, verbose_name='التاريخ')
    serial_number = models.PositiveIntegerField(default=0, verbose_name='المسلسل')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='account_transfers', verbose_name='بواسطة',
    )

    class Meta:
        verbose_name = 'تحويل حساب'
        verbose_name_plural = 'تحويلات الحسابات'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'serial_number'],
                name='unique_branch_transfer_serial',
            ),
        ]

    def __str__(self):
        return f'تحويل #{self.serial_number} — {self.get_direction_display()} — {self.amount}'

    @classmethod
    def next_serial(cls, branch):
        from django.db.models import Max
        last = cls.objects.filter(branch=branch).aggregate(m=Max('serial_number'))['m'] or 0
        return last + 1

    def save(self, *args, **kwargs):
        if self.branch_id and not self.serial_number:
            self.serial_number = AccountTransfer.next_serial(self.branch)
        super().save(*args, **kwargs)