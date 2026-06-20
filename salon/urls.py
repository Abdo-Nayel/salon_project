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
    path('send-whatsapp/', views.send_whatsapp_invoice, name='send_whatsapp_invoice'),
    path('pos/get-invoice/<int:invoice_id>/', views.get_invoice_json, name='get_invoice_json'),
    path('pos/lookup/', views.pos_lookup_invoice, name='pos_lookup_invoice'),
    path('pos/booking/', views.pos_lookup_booking, name='pos_lookup_booking'),
    path('pos/void/<int:pk>/', views.pos_void_invoice, name='pos_void_invoice'),

    # Bookings
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/add/', views.booking_add, name='booking_add'),
    path('bookings/<int:pk>/status/', views.booking_status, name='booking_status'),
    path('queue/print-number/', views.print_queue_number, name='print_queue_number'),
    path('queue/receipt/', views.print_simple_queue_receipt, name='print_simple_queue'),

    # Inventory (أصناف + مشتريات + تقرير)
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/item/add/', views.inventory_item_add, name='inventory_item_add'),
    path('inventory/item/lookup/', views.inventory_item_lookup, name='inventory_item_lookup'),
    path('inventory/purchase/add/', views.inventory_purchase_add, name='inventory_purchase_add'),
    path('inventory/purchase/lookup/', views.inventory_purchase_lookup, name='inventory_purchase_lookup'),
    path('inventory/purchase/<int:pk>/delete/', views.inventory_purchase_delete, name='inventory_purchase_delete'),
    path('inventory/consumption/add/', views.inventory_consumption_add, name='inventory_consumption_add'),
    path('inventory/consumption/lookup/', views.inventory_consumption_lookup, name='inventory_consumption_lookup'),
    path('inventory/consumption/<int:pk>/delete/', views.inventory_consumption_delete, name='inventory_consumption_delete'),
    path('inventory/report/', views.inventory_report, name='inventory_report'),
    path('inventory/report/pdf/', views.inventory_report_pdf, name='inventory_report_pdf'),
    path('inventory/totals/', views.inventory_totals, name='inventory_totals'),
    path('inventory/totals/pdf/', views.inventory_totals_pdf, name='inventory_totals_pdf'),
    path('inventory/purchase/<int:pk>/', views.inventory_purchase_detail, name='inventory_purchase_detail'),
    path('inventory/movement/add/', views.stock_movement_add, name='stock_movement_add'),

    # Expenses
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/type/add/', views.expense_type_add, name='expense_type_add'),
    path('expenses/type/lookup/', views.expense_type_lookup, name='expense_type_lookup'),
    path('expenses/out/add/', views.expense_out_add, name='expense_out_add'),
    path('expenses/out/lookup/', views.expense_out_lookup, name='expense_out_lookup'),
    path('expenses/out/<int:pk>/delete/', views.expense_out_delete, name='expense_out_delete'),
    path('expenses/return/add/', views.expense_return_add, name='expense_return_add'),
    path('expenses/return/lookup/', views.expense_return_lookup, name='expense_return_lookup'),
    path('expenses/return/<int:pk>/delete/', views.expense_return_delete, name='expense_return_delete'),
    path('expenses/add/', views.expense_add, name='expense_add'),

    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/pdf/', views.reports_pdf, name='reports_pdf'),
    path('reports/activity-log/', views.activity_log, name='activity_log'),
    path('reports/account-statement/', views.account_statement, name='account_statement'),
    path('reports/account-transfer/', views.account_transfer_save, name='account_transfer_save'),

    # Services
    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.service_add, name='service_add'),
    path('services/lookup/', views.service_lookup, name='service_lookup'),

    # Products (kept for inventory use, removed from menu)
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),

    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_add, name='customer_add'),

    # Employees
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/lookup/', views.employee_lookup, name='employee_lookup'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
    path('settings/backup/', views.settings_backup, name='settings_backup'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/lookup/', views.user_lookup, name='user_lookup'),
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