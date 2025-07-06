# passenger_wsgi.py
import sys, os

# Replace with your correct path
sys.path.insert(0, '/home/justlilbling/ecom')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecom.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
