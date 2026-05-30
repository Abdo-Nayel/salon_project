"""
Salon Pro URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # POS
    path('pos/', views.pos, name='pos'),
    path('invoice/<int:pk>/print/', views.invoice_print, name='invoice_print'),
    path('pos/send-whatsapp/', views.send_whatsapp_invoice, name='send_whatsapp_invoice'),

    # Bookings
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/add/', views.booking_add, name='booking_add'),
    path('bookings/<int:pk>/status/', views.booking_status, name='booking_status'),
    path('queue/print-number/', views.print_queue_number, name='print_queue_number'),

    # Inventory
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/movement/add/', views.stock_movement_add, name='stock_movement_add'),

    # Expenses
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.expense_add, name='expense_add'),

    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/pdf/', views.reports_pdf, name='reports_pdf'),

    # Services
    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.service_add, name='service_add'),

    # Products (kept for inventory use, removed from menu)
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),

    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_add, name='customer_add'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # Branches
    path('branches/', views.branch_list, name='branch_list'),
    path('branches/add/', views.branch_add, name='branch_add'),

    # Banks
    path('banks/', views.bank_list, name='bank_list'),
    path('banks/add/', views.bank_add, name='bank_add'),

    # Printing
    path('booking/<int:pk>/print/', views.print_queue_ticket, name='print_queue_ticket'),
    path('invoice/<int:pk>/receipt/', views.print_invoice_receipt, name='print_invoice_receipt'),
    path('booking/<int:pk>/print-direct/', views.print_direct_queue, name='print_direct_queue'),
    path('invoice/<int:pk>/print-direct/', views.print_direct_invoice, name='print_direct_invoice'),

    # API
    path('api/search-customer/', views.api_search_customer, name='api_search_customer'),
    path('api/service-search/', views.api_service_search, name='api_service_search'),
]