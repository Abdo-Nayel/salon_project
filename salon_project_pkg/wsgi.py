"""
WSGI config for salon_project
"""
import os
import sys

# Add project to path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon_project_pkg.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
