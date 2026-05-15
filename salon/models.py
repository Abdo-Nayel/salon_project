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


# =============================================================================
# USERS & PERMISSIONS
# =============================================================================

class User(AbstractUser):
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='users', verbose_name="Branch"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    photo = models.ImageField(upload_to='users/', blank=True, verbose_name="Photo")
    is_barber = models.BooleanField(default=False, verbose_name="Is Barber")
    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, null=True, blank=True,
        verbose_name="Commission %"
    )

    # Permissions
    can_pos = models.BooleanField(default=True, verbose_name="Can Access POS")
    can_inventory = models.BooleanField(default=True, verbose_name="Can Access Inventory")
    can_expenses = models.BooleanField(default=True, verbose_name="Can Access Expenses")
    can_reports = models.BooleanField(default=True, verbose_name="Can Access Reports")
    can_settings = models.BooleanField(default=False, verbose_name="Can Access Settings")
    can_users = models.BooleanField(default=False, verbose_name="Can Manage Users")

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
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='services',
        verbose_name="Branch"
    )
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
    invoice_number = models.CharField(max_length=20, unique=True, verbose_name="Invoice #")

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

    def __str__(self):
        return f"INV-{self.invoice_number} - {self.final_total} EGP"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        self.final_total = self.subtotal - self.discount + self.tax
        super().save(*args, **kwargs)

    def generate_invoice_number(self):
        prefix = f"{self.branch.id}-{timezone.now().strftime('%Y%m%d')}"
        count = Invoice.objects.filter(invoice_number__startswith=prefix).count()
        return f"{prefix}-{count + 1:04d}"


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
    queue_number = models.PositiveIntegerField(verbose_name="Queue #")
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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product} - {self.get_movement_type_display()} {self.quantity}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.movement_type == 'in':
            self.product.stock += self.quantity
        elif self.movement_type == 'out':
            self.product.stock -= self.quantity
        self.product.save()