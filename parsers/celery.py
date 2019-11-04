import os
from celery import Celery
from celery import task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parsers.settings')

app = Celery('parsers',include=['app.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
