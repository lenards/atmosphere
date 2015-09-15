from atmosphere import settings
import traceback
from core.logging import create_celery_logger
from celery.signals import after_setup_task_logger, task_failure

CELERY_LOG = None

@after_setup_task_logger.connect
def modify_celery_logger(**kwargs):
    """
    Step 1/2 completed -- Still need to add CeleryAdapter from above
    """
    global CELERY_LOG
    if not settings.has_logstash:
        CELERY_LOG = kwargs.get('logger')
        return
    from atmosphere.settings import LOGSTASH_HANDLER
    logger = kwargs.get('logger')
    logger.addHandler(LOGSTASH_HANDLER)
    CELERY_LOG = create_celery_logger(logger, **{"type": "celery"})


@task_failure.connect
def log_task_failure(**kwargs):
    log_dict = kwargs.copy()
    log_dict['task_args'] = log_dict.pop('args')
    log_dict['task_kwargs'] = log_dict.pop('kwargs')
    tb = log_dict.pop('traceback')
    tb_list = traceback.format_tb(tb)
    log_dict['traceback'] = ' '.join(tb_list)
    task_id = kwargs.get('task_id')
    exc  = kwargs.get('exception')
    # ".pop" things we dont want
    CELERY_LOG.error("Celery Task Failed - ID: %s Error Message: %s" % (task_id, exc.message), extra=log_dict)

def get_celery_log():
    return CELERY_LOG
