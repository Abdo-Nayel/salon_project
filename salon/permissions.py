"""Granular user permissions — groups for UI and helpers for views."""

USER_PERMISSION_FIELDS = (
    'can_pos', 'can_delete_pos',
    'can_bookings', 'can_booking_vip', 'can_booking_queue', 'can_delete_bookings',
    'can_inventory', 'can_inv_items', 'can_inv_purchase', 'can_inv_consumption',
    'can_inv_report', 'can_inv_totals', 'can_delete_inventory',
    'can_expenses', 'can_expense_types', 'can_expense_out', 'can_expense_return',
    'can_delete_expenses',
    'can_reports', 'can_report_activity', 'can_report_statement',
    'can_services', 'can_delete_services',
    'can_customers',
    'can_employees', 'can_delete_employees',
    'can_settings', 'can_users',
)

# access = صلاحية الدخول للصفحة (تُفعّل تلقائياً مع القسم الرئيسي)
# subs = ما يظهر داخل الشاشة فقط (تكويد، حذف، …)
PERMISSION_GROUPS = [
    {
        'parent': 'can_pos',
        'access': 'can_pos',
        'label': 'نقطة البيع',
        'subs': [
            {'field': 'can_delete_pos', 'label': 'حذف / إلغاء فاتورة', 'delete': True},
        ],
    },
    {
        'parent': 'can_bookings',
        'access': 'can_bookings',
        'label': 'الحجوزات',
        'subs': [
            {'field': 'can_booking_vip', 'label': 'حجز VIP'},
            {'field': 'can_booking_queue', 'label': 'طباعة رقم دور'},
            {'field': 'can_delete_bookings', 'label': 'حذف حجز', 'delete': True},
        ],
    },
    {
        'parent': 'can_inventory',
        'access': 'can_inventory',
        'label': 'المخزن',
        'subs': [
            {'field': 'can_inv_items', 'label': 'تكويد / إضافة صنف'},
            {'field': 'can_inv_purchase', 'label': 'مشتريات صنف'},
            {'field': 'can_inv_consumption', 'label': 'أصناف مستهلكة'},
            {'field': 'can_inv_report', 'label': 'تقرير حركة المخزن'},
            {'field': 'can_inv_totals', 'label': 'صافي إجماليات المخزون'},
            {'field': 'can_delete_inventory', 'label': 'حذف حركات مخزن', 'delete': True},
        ],
    },
    {
        'parent': 'can_expenses',
        'access': 'can_expenses',
        'label': 'المصروفات',
        'subs': [
            {'field': 'can_expense_types', 'label': 'تكويد مصروف'},
            {'field': 'can_expense_out', 'label': 'مصروف'},
            {'field': 'can_expense_return', 'label': 'مرتد مصروف'},
            {'field': 'can_delete_expenses', 'label': 'حذف سند مصروف', 'delete': True},
        ],
    },
    {
        'parent': 'can_reports',
        'access': 'can_reports',
        'label': 'التقارير',
        'subs': [
            {'field': 'can_report_activity', 'label': 'سجل الحركات'},
            {'field': 'can_report_statement', 'label': 'كشف الحسابات'},
        ],
    },
    {
        'parent': 'can_services',
        'access': 'can_services',
        'label': 'الخدمات',
        'subs': [
            {'field': 'can_delete_services', 'label': 'حذف خدمة', 'delete': True},
        ],
    },
    {
        'parent': 'can_customers',
        'access': 'can_customers',
        'label': 'العملاء',
        'subs': [],
    },
    {
        'parent': 'can_employees',
        'access': 'can_employees',
        'label': 'الموظفين',
        'subs': [
            {'field': 'can_delete_employees', 'label': 'حذف موظف', 'delete': True},
        ],
    },
    {
        'parent': 'can_settings',
        'access': 'can_settings',
        'label': 'الإعدادات',
        'includes_users': True,
        'subs': [],
    },
]

MODULE_MENU_FIELDS = {
    'pos': ('can_pos',),
    'bookings': ('can_bookings', 'can_booking_vip', 'can_booking_queue'),
    'inventory': (
        'can_inventory', 'can_inv_items', 'can_inv_purchase', 'can_inv_consumption',
        'can_inv_report', 'can_inv_totals',
    ),
    'expenses': ('can_expenses', 'can_expense_types', 'can_expense_out', 'can_expense_return'),
    'reports': ('can_reports', 'can_report_activity', 'can_report_statement'),
    'services': ('can_services',),
    'customers': ('can_customers',),
    'employees': ('can_employees',),
    'settings': ('can_settings', 'can_users'),
}


def has_perm(user, field):
    if not user or not getattr(user, 'is_authenticated', False):
        return False
    if user.is_superuser:
        return True
    return bool(getattr(user, field, False))


def permissions_dict(user):
    if not user or not user.is_authenticated:
        return {}
    if user.is_superuser:
        perms = {f: True for f in USER_PERMISSION_FIELDS}
    else:
        perms = {f: bool(getattr(user, f, False)) for f in USER_PERMISSION_FIELDS}
    for menu_key, fields in MODULE_MENU_FIELDS.items():
        perms[f'menu_{menu_key}'] = any(perms.get(f) for f in fields)
    return perms


def apply_user_permissions(user, data):
    for field in USER_PERMISSION_FIELDS:
        setattr(user, field, bool(data.get(field)))
    if user.can_settings:
        user.can_users = True
    else:
        user.can_users = bool(data.get('can_users'))


def user_permissions_payload(user):
    payload = permissions_dict(user)
    payload['is_active'] = user.is_active
    return payload
