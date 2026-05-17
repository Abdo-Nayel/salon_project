"""
Salon Admin
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Branch, User, Category, Service, Product, Bank, Customer,
    Invoice, InvoiceItem, Booking, Expense, StockMovement
)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_main', 'is_active']
    list_filter = ['is_main', 'is_active']
    search_fields = ['name']


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'branch', 'is_barber', 'is_superuser']
    list_filter = ['branch', 'is_barber', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        ('Salon Info', {
            'fields': ('branch', 'phone', 'photo', 'is_barber', 'commission_rate')
        }),
        ('Permissions', {
            'fields': ('can_pos', 'can_inventory', 'can_expenses', 'can_reports', 'can_settings', 'can_users')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'icon', 'is_active']
    list_filter = ['type', 'is_active']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'code']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'code']


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['name', 'account_number', 'branch', 'is_active']
    list_filter = ['branch', 'is_active']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'branch', 'visits_count', 'total_spent']
    list_filter = ['branch']
    search_fields = ['name', 'phone']


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'branch', 'customer', 'barber', 'final_total', 'payment_method', 'created_at']
    list_filter = ['branch', 'payment_method', 'created_at']
    search_fields = ['invoice_number', 'customer__name']
    inlines = [InvoiceItemInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['queue_number', 'customer_name', 'branch', 'barber', 'status', 'created_at']
    list_filter = ['branch', 'status']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['category', 'branch', 'amount', 'date', 'created_by']
    list_filter = ['branch', 'category', 'date']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'date', 'branch']
    list_filter = ['branch', 'movement_type']
