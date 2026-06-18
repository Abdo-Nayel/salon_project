"""
Salon Context Processors
"""
from django.conf import settings


def branch_context(request):
    """Add branch context to all templates"""
    context = {
        'project_vendor': getattr(settings, 'PROJECT_VENDOR', 'LyomasTech'),
    }

    if request.user.is_authenticated:
        context['user_branch'] = request.user.branch
        context['is_admin'] = request.user.is_admin
        context['user_permissions'] = {
            'can_pos': request.user.can_pos,
            'can_inventory': request.user.can_inventory,
            'can_expenses': request.user.can_expenses,
            'can_reports': request.user.can_reports,
            'can_settings': request.user.can_settings,
            'can_bookings': request.user.can_bookings,
            'can_customers': request.user.can_customers,
            'can_services': request.user.can_services,
        }

    return context
