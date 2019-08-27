"""
WSGI config for WebDemo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""
import sys
sys.path.append('/usr/local/lib/python3.7/;/usr/local/lib/python3.7/site-packages;/usr/local/lib/python3.7/lib-dynloadexport')
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebDemo.settings')

application = get_wsgi_application()
