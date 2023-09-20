from logic.adapters.task import TaskAdapter
from celery.result import AsyncResult
import datetime
from utilities.logging import logger
import time
from core.celery import app
import json



class BaseOrganizer:
    """
    Base class for TaskOrganizer.
    """

    def __init__(self, *args, **kwargs):
        self.task_adapter = TaskAdapter()
        self.logger = logger 

    def generate_date_from_timestamp(self, timestamp: int):
        """
        Convert timestamp to datetime object.
        """
        date_object = datetime.datetime.fromtimestamp(timestamp)
        return date_object
    
    def generate_timedelta_day(self, task_frequency: int):
        """
        Generate a timedelta from Task's frequency.
        """
        time_delta = datetime.timedelta(days=task_frequency)
        return time_delta

    def generate_current_timestamp(self):
        """
        Generate timestamp of current date.
        """
        now = int(time.time())
        return now

    def start_inspect(self):
        """
        Returns inspect object for current Celery app.
        """
        return app.control.inspect()
