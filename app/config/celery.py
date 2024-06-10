import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = Celery('config')
application.config_from_object('django.conf:settings', namespace='CELERY')

application.autodiscover_tasks()
