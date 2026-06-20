"""
Salon Context Processors
"""
from django.conf import settings


def branch_context(request):
    """Add branch context to all templates"""
    from .models import SalonSettings
    from .permissions import permissions_dict

    salon = SalonSettings.get()
    salon_display_name = salon.salon_name or getattr(settings, 'PROJECT_NAME', 'LyomasTech')

    context = {
        'project_vendor': getattr(settings, 'PROJECT_VENDOR', 'LyomasTech'),
        'project_name': getattr(settings, 'PROJECT_NAME', 'LyomasTech'),
        'brand_logo': getattr(settings, 'BRAND_LOGO', 'salon/LyomasTech_Logo2.png'),
        'salon_display_name': salon_display_name,
    }

    if request.user.is_authenticated:
        context['user_branch'] = request.user.branch
        context['is_admin'] = request.user.is_admin
        context['user_permissions'] = permissions_dict(request.user)

    return context
