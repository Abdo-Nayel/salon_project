"""
Salon Pro - Minimal Printer Module
Falls back to browser printing if Windows printing is not available
"""
import os
from django.conf import settings
from django.template.loader import render_to_string


def print_queue_ticket(queue_number, customer_name='', barber_name='', services=None, estimated_total=0):
    """Print queue ticket - returns HTML for browser printing"""
    config = {
        'shop_name': getattr(settings, 'SALON_NAME', 'Salon Pro'),
        'shop_phone': getattr(settings, 'SALON_PHONE', ''),
        'shop_address': getattr(settings, 'SALON_ADDRESS', ''),
        'footer_text': 'شكراً لزيارتكم!',
    }

    html = render_to_string('salon/queue_receipt.html', {
        'queue_number': queue_number,
        'customer_name': customer_name,
        'barber_name': barber_name,
        'services': services or [],
        'estimated_total': estimated_total,
        'config': config,
    })

    return True, html


def print_invoice_receipt(invoice, items):
    """Print invoice receipt - returns HTML for browser printing"""
    config = {
        'shop_name': getattr(settings, 'SALON_NAME', 'Salon Pro'),
        'shop_phone': getattr(settings, 'SALON_PHONE', ''),
        'shop_address': getattr(settings, 'SALON_ADDRESS', ''),
        'footer_text': 'شكراً لزيارتكم!',
    }

    html = render_to_string('salon/invoice_receipt.html', {
        'invoice': invoice,
        'items': items,
        'config': config,
    })

    return True, html