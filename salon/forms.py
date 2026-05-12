"""
Salon Pro Forms
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import (
    Branch, User, Category, Service, Product, Bank, Customer,
    Invoice, InvoiceItem, Booking, Expense, StockMovement
)


# =============================================================================
# AUTH FORMS
# =============================================================================

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسم المستخدم'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'كلمة المرور'
        })
    )


# =============================================================================
# USER FORMS
# =============================================================================

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 
                  'branch', 'is_barber', 'commission_rate',
                  'can_pos', 'can_inventory', 'can_expenses', 'can_reports', 
                  'can_settings', 'can_users', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'is_barber': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'commission_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'can_pos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_inventory': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_expenses': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_reports': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_settings': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_users': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# =============================================================================
# BRANCH FORMS
# =============================================================================

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'address', 'phone', 'is_main', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# =============================================================================
# SERVICE FORMS (NO CATEGORY)
# =============================================================================

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'code', 'price', 'cost', 'duration', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# =============================================================================
# PRODUCT FORMS (NO CATEGORY)
# =============================================================================

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'price', 'cost', 'stock', 'min_stock', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# =============================================================================
# BANK FORMS
# =============================================================================

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'account_number', 'branch', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# =============================================================================
# CUSTOMER FORMS
# =============================================================================

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# =============================================================================
# BOOKING FORMS
# =============================================================================

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_phone', 'services', 'barber', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'barber': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# =============================================================================
# EXPENSE FORMS (NO CATEGORY)
# =============================================================================

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'date', 'receipt']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'receipt': forms.FileInput(attrs={'class': 'form-control'}),
        }


# =============================================================================
# STOCK MOVEMENT FORMS
# =============================================================================

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'cost', 'notes', 'date']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'movement_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }