"""
BaseClass for Celery Tasks

To be used by Celery Tasks ONLY!
"""
from celery import Task
from service.task_signals import get_celery_log

class CloudTask(Task):
    abstract = True
    _logger = None

    @property
    def logger(self):
        if self._logger is None:
            self._logger = get_celery_log()
        return self._logger
