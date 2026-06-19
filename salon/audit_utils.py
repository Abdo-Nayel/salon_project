"""Audit trail helpers for سجل الحركات."""

ACTION_CREATE = 'create'
ACTION_UPDATE = 'update'
ACTION_DELETE = 'delete'
ACTION_VOID = 'void'

T_INVOICE = 'فاتورة مبيعات'
T_BOOKING = 'حجز'
T_PRODUCT = 'صنف مخزون'
T_PURCHASE = 'فاتورة مشتريات'
T_CONSUMPTION = 'فاتورة استهلاك'
T_EXPENSE_TYPE = 'نوع مصروف'
T_EXPENSE_VOUCHER = 'سند مصروف'
T_SERVICE = 'خدمة'
T_CUSTOMER = 'عميل'
T_EMPLOYEE = 'موظف'
T_USER = 'مستخدم'
T_STOCK = 'حركة مخزون'
T_SETTINGS = 'إعدادات'
T_BACKUP = 'نسخ احتياطي'


def _resolve_branch(request, branch):
    if branch is not None:
        return branch
    user = getattr(request, 'user', None)
    if user and user.is_authenticated and not user.is_superuser:
        return getattr(user, 'branch', None)
    return None


def log_activity(request, action, entity_type, entity_label, entity_id=None, branch=None, details=''):
    """Record create / update / delete / void in activity log."""
    from .models import ActivityLog

    user = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None
    label = (entity_label or '')[:255]
    ActivityLog.objects.create(
        user=user,
        branch=_resolve_branch(request, branch),
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        entity_label=label,
        details=(details or '')[:2000],
    )
