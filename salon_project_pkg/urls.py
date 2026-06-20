"""
Project URLs
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView

_brand_logo = getattr(settings, 'BRAND_LOGO', 'salon/LyomasTech_Logo2.png')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('salon.urls')),
    path(
        'favicon.ico',
        RedirectView.as_view(url=staticfiles_storage.url(_brand_logo), permanent=True),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
