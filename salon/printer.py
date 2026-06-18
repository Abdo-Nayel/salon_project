"""
Salon Pro - Minimal Printer Module
Falls back to browser printing if Windows printing is not available
"""
from django.template.loader import render_to_string

from .models import SalonSettings


def _print_config(request=None):
    return SalonSettings.get().print_config(request)


def print_queue_ticket(queue_number, customer_name='', employee_name='', services=None, estimated_total=0, request=None, barber_name=''):
    """Print queue ticket - returns HTML for browser printing"""
    staff_name = employee_name or barber_name
    html = render_to_string('salon/queue_receipt.html', {
        'queue_number': queue_number,
        'customer_name': customer_name,
        'employee_name': staff_name,
        'services': services or [],
        'estimated_total': estimated_total,
        'config': _print_config(request),
    })
    return True, html


def print_invoice_receipt(invoice, items, request=None):
    """Print invoice receipt - returns HTML for browser printing"""
    html = render_to_string('salon/invoice_receipt.html', {
        'invoice': invoice,
        'items': items,
        'config': _print_config(request),
    })
    return True, html
