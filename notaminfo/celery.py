import os

from django.conf import settings

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notaminfo.settings')

app = Celery('proj')

app.config_from_object(f'django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
