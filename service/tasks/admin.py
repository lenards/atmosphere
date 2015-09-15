from celery.decorators import task

from core.email import send_approved_resource_email
from core.models import ResourceRequest
from core.models.status_type import get_status_type

from service.base import CloudTask
from service.quota import set_provider_quota as spq


@task(bind=True, base=CloudTask, name="set_provider_quota",
      default_retry_delay=5,
      time_limit=30 * 60,  # 30minute hard-set time limit.
      max_retries=3)
def set_provider_quota(self, identity_uuid):
    try:
        spq(identity_uuid)
    except Exception as exc:
        self.logger.exception(
            "Encountered an exception trying to "
            "'set_provider_quota' for Identity UUID:%s"
            % identity_uuid)
        set_provider_quota.retry(exc=exc)


@task(bind=True, base=CloudTask, name="close_resource_request")
def close_resource_request(self, res, identifier):
    """
    Close the request and email approval message
    """
    instance = ResourceRequest.objects.get(id=identifier)
    instance.status = get_status_type(status="closed")
    instance.save()
    send_approved_resource_email(user=instance.created_by,
                                 request=instance.request,
                                 reason=instance.admin_message)


@task(bind=True, base=CloudTask, name='set_resource_request_failed')
def set_resource_request_failed(self, err, identifier):
    """
    Set the quota request as failed if
    Marks the quota request ask
    """
    request = ResourceRequest.objects.get(id=identifier)
    request.status = get_status_type(status="failed")
    request.save()
