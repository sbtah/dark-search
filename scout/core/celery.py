import os

from celery import Celery
from celery.utils.log import get_task_logger
from django.conf import settings
from utilities.logging import logger

# Set the default Django settings module for the celery app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


app = Celery('core')
logger = get_task_logger(logger)

# Read config from Django settings, the 'CELERY' namespace would make celery
# - config keys has 'CELERY' prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Discover and load tasks from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# Test task
@app.task
def divide(x, y):
    import time

    time.sleep(5)
    return x // y
