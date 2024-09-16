import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'Test_grocery_store_Sarafan.settings'
)

application = get_wsgi_application()
