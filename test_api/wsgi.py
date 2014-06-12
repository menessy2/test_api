"""
WSGI config for test_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os ,  sys

sys.path.append('/var/www/html/test_api')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_api.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
