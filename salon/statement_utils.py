"""Account statement (كشف الحسابات) helpers."""
from decimal import Decimal

from .models import Branch, ExpenseVoucher, Invoice


def get_statement_branch(request):
    """Branch filter for statements. None = all branches (superuser / main branch)."""
    if getattr(request.user, 'can_see_all_branches', False):
        branch_id = request.GET.get('branch', '').strip()
        if branch_id.isdigit():
            return Branch.objects.filter(id=int(branch_id), is_active=True).first()
        return None
    return getattr(request.user, 'branch', None)


def get_active_banks():
    from .models import Bank
    return Bank.objects.filter(is_active=True).order_by('name')


def _invoice_qs(branch, start_date, end_date):
    qs = Invoice.objects.filter(is_voided=False).select_related('bank', 'branch')
    if branch:
        qs = qs.filter(branch=branch)
    if start_date and end_date:
        qs = qs.filter(created_at__date__range=[start_date, end_date])
    return qs


def _voucher_qs(branch, start_date, end_date):
    qs = ExpenseVoucher.objects.select_related(
        'expense_type', 'bank', 'branch', 'created_by',
    )
    if branch:
        qs = qs.filter(branch=branch)
    if start_date and end_date:
        qs = qs.filter(date__range=[start_date, end_date])
    return qs


def _transfer_qs(branch, start_date, end_date, bank_id=None):
    from .models import AccountTransfer
    qs = AccountTransfer.objects.select_related('bank', 'branch', 'created_by')
    if branch:
        qs = qs.filter(branch=branch)
    if start_date and end_date:
        qs = qs.filter(date__range=[start_date, end_date])
    if bank_id:
        qs = qs.filter(bank_id=bank_id)
    return qs


def build_cash_statement(branch, start_date, end_date):
    rows = []
    total_in = Decimal('0')
    total_out = Decimal('0')

    for inv in _invoice_qs(branch, start_date, end_date).filter(payment_method='cash'):
        rows.append({
            'date': inv.created_at,
            'sort_date': inv.created_at.date(),
            'type': 'فاتورة مبيعات',
            'ref': f'#{inv.display_number()}',
            'description': inv.customer.name if inv.customer else '—',
            'in_amount': inv.final_total,
            'out_amount': Decimal('0'),
            'branch': inv.branch.name if inv.branch else '—',
        })
        total_in += inv.final_total

    for v in _voucher_qs(branch, start_date, end_date).filter(
        payment_method='cash', voucher_type='out',
    ):
        rows.append({
            'date': v.created_at,
            'sort_date': v.date,
            'type': 'مصروف',
            'ref': f'#{v.serial_number}',
            'description': v.expense_type.name,
            'in_amount': Decimal('0'),
            'out_amount': v.amount,
            'branch': v.branch.name if v.branch else '—',
            'notes': v.notes,
        })
        total_out += v.amount

    for v in _voucher_qs(branch, start_date, end_date).filter(
        payment_method='cash', voucher_type='return',
    ):
        rows.append({
            'date': v.created_at,
            'sort_date': v.date,
            'type': 'مرتد مصروف',
            'ref': f'#{v.serial_number}',
            'description': v.expense_type.name,
            'in_amount': v.amount,
            'out_amount': Decimal('0'),
            'branch': v.branch.name if v.branch else '—',
            'notes': v.notes,
        })
        total_in += v.amount

    for t in _transfer_qs(branch, start_date, end_date):
        if t.direction == 'cash_to_bank':
            rows.append({
                'date': t.created_at,
                'sort_date': t.date,
                'type': 'تحويل → بنك',
                'ref': f'#{t.serial_number}',
                'description': t.bank.name,
                'in_amount': Decimal('0'),
                'out_amount': t.amount,
                'branch': t.branch.name if t.branch else '—',
                'notes': t.notes,
            })
            total_out += t.amount
        else:
            rows.append({
                'date': t.created_at,
                'sort_date': t.date,
                'type': 'تحويل ← بنك',
                'ref': f'#{t.serial_number}',
                'description': t.bank.name,
                'in_amount': t.amount,
                'out_amount': Decimal('0'),
                'branch': t.branch.name if t.branch else '—',
                'notes': t.notes,
            })
            total_in += t.amount

    rows.sort(key=lambda r: (r['sort_date'], r['date']))
    balance = total_in - total_out
    return {
        'rows': rows,
        'total_in': total_in,
        'total_out': total_out,
        'balance': balance,
    }


def build_bank_statement(branch, start_date, end_date, bank_id=None):
    rows = []
    total_in = Decimal('0')
    total_out = Decimal('0')

    inv_qs = _invoice_qs(branch, start_date, end_date).filter(payment_method='bank')
    if bank_id:
        inv_qs = inv_qs.filter(bank_id=bank_id)

    for inv in inv_qs:
        rows.append({
            'date': inv.created_at,
            'sort_date': inv.created_at.date(),
            'type': 'فاتورة مبيعات',
            'ref': f'#{inv.display_number()}',
            'description': inv.customer.name if inv.customer else '—',
            'bank': inv.bank.name if inv.bank else '—',
            'in_amount': inv.final_total,
            'out_amount': Decimal('0'),
            'branch': inv.branch.name if inv.branch else '—',
        })
        total_in += inv.final_total

    v_qs = _voucher_qs(branch, start_date, end_date).filter(payment_method='bank')
    if bank_id:
        v_qs = v_qs.filter(bank_id=bank_id)

    for v in v_qs.filter(voucher_type='out'):
        rows.append({
            'date': v.created_at,
            'sort_date': v.date,
            'type': 'مصروف',
            'ref': f'#{v.serial_number}',
            'description': v.expense_type.name,
            'bank': v.bank.name if v.bank else '—',
            'in_amount': Decimal('0'),
            'out_amount': v.amount,
            'branch': v.branch.name if v.branch else '—',
            'notes': v.notes,
        })
        total_out += v.amount

    for v in v_qs.filter(voucher_type='return'):
        rows.append({
            'date': v.created_at,
            'sort_date': v.date,
            'type': 'مرتد مصروف',
            'ref': f'#{v.serial_number}',
            'description': v.expense_type.name,
            'bank': v.bank.name if v.bank else '—',
            'in_amount': v.amount,
            'out_amount': Decimal('0'),
            'branch': v.branch.name if v.branch else '—',
            'notes': v.notes,
        })
        total_in += v.amount

    for t in _transfer_qs(branch, start_date, end_date, bank_id):
        if t.direction == 'cash_to_bank':
            rows.append({
                'date': t.created_at,
                'sort_date': t.date,
                'type': 'تحويل ← نقدية',
                'ref': f'#{t.serial_number}',
                'description': t.notes or 'إيداع من النقدية',
                'bank': t.bank.name,
                'in_amount': t.amount,
                'out_amount': Decimal('0'),
                'branch': t.branch.name if t.branch else '—',
                'notes': t.notes,
            })
            total_in += t.amount
        else:
            rows.append({
                'date': t.created_at,
                'sort_date': t.date,
                'type': 'تحويل → نقدية',
                'ref': f'#{t.serial_number}',
                'description': t.notes or 'سحب إلى النقدية',
                'bank': t.bank.name,
                'in_amount': Decimal('0'),
                'out_amount': t.amount,
                'branch': t.branch.name if t.branch else '—',
                'notes': t.notes,
            })
            total_out += t.amount

    rows.sort(key=lambda r: (r['sort_date'], r['date']))
    return {
        'rows': rows,
        'total_in': total_in,
        'total_out': total_out,
        'balance': total_in - total_out,
    }


def build_transfer_statement(branch, start_date, end_date, bank_id=None):
    rows = []
    total_in = Decimal('0')
    total_out = Decimal('0')

    for t in _transfer_qs(branch, start_date, end_date, bank_id):
        rows.append({
            'date': t.created_at,
            'sort_date': t.date,
            'type': t.get_direction_display(),
            'ref': f'#{t.serial_number}',
            'description': t.notes or t.bank.name,
            'bank': t.bank.name,
            'branch': t.branch.name if t.branch else '—',
            'notes': t.notes,
            'in_amount': t.amount,
            'out_amount': t.amount,
            'direction': t.direction,
        })
        total_in += t.amount
        total_out += t.amount

    rows.sort(key=lambda r: (r['sort_date'], r['date']))
    return {
        'rows': rows,
        'total_in': total_in,
        'total_out': total_out,
        'balance': total_in - total_out,
    }
