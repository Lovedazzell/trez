import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bit.settings')

app = Celery('bit')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    't_m_count':{
        'task':'core.tasks.countdown_handel',
        'schedule':crontab(minute='*/3')
    }
}
# Load task modules from all registered Django apps.
app.autodiscover_tasks()