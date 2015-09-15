from __future__ import absolute_import
from atmosphere.settings import LOGSTASH_HANDLER
import logging


class InstanceAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):
        extra = kwargs.get("extra", {})
        extra.update(self.extra)
        kwargs["extra"] = extra
        fields = "|".join([self.extra['instance_id'],
                           self.extra['ip_address'],
                           self.extra['username']])
        return '%s %s' % (fields, msg), kwargs


def create_instance_logger(logger, ip_address, username, instance_id):
    adapter = InstanceAdapter(logger, {'instance_id': instance_id,
                                       'ip_address': ip_address,
                                       'type': "atmo-deploy",
                                       'username': username})
    return adapter

class CeleryAdapter(logging.LoggerAdapter):

    def warn(self, *args, **kwargs):
        return self.warning(*args, **kwargs)
    #def warn(self, *args, **kwargs):
    #    return self.logger.warn(*args, **kwargs)

    def process(self, msg, kwargs):
        #TODO: Celery specific stuff in here
        extra = kwargs.get("extra", {})
        extra.update(self.extra)
        kwargs["extra"] = extra
        #fields = "|".join([self.extra['instance_id'],
        #                   self.extra['ip_address'],
        #                   self.extra['username']])
        #return '%s %s' % (fields, msg), kwargs
        # NOTE: Prints message w/kwargs && returns kwargs
        return '%s %s' % (msg,kwargs), kwargs


def create_celery_logger(logger, **kwargs):
    adapter = CeleryAdapter(logger, kwargs)  # Make it a dict!
    return adapter

