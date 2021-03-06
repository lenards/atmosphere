"""
Atmosphere api email
"""
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from threepio import logger

from iplantauth.protocol.ldap import lookupEmail

from core.email import email_admin, feedback_email, resource_request_email

from api import failure_response
from api.v1.views.base import AuthAPIView


class Feedback(AuthAPIView):

    """
    Post feedback via RESTful API
    """

    def post(self, request):
        """
        Creates a new feedback email and sends it to admins.
        """
        required = ["message","user-interface"]
        missing_keys = check_missing_keys(request.DATA, required)
        if missing_keys:
            return keys_not_found(missing_keys)
        result = self._email(request,
                             request.user.username,
                             lookupEmail(request.user.username),
                             request.DATA["message"],
                             request.DATA)
        return Response(result, status=status.HTTP_201_CREATED)

    def _email(self, request, username, user_email, message, data):
        """
        Sends an email Bto support based on feedback from a client machine

        Returns a response.
        """
        data['server'] = settings.SERVER_URL
        return feedback_email(request, username, user_email, message, data)


class QuotaEmail(AuthAPIView):

    """
    Post Quota Email via RESTful API.
    """

    def post(self, request):
        """
        Creates a new Quota Request email and sends it to admins.
        """
        required = ["quota", "reason"]
        missing_keys = check_missing_keys(request.DATA, required)
        if missing_keys:
            return keys_not_found(missing_keys)
        logger.debug("request.DATA = %s" % (str(request.DATA)))
        result = self._email(request,
                             request.user.username,
                             request.DATA["quota"],
                             request.DATA["reason"])
        return Response(result, status=status.HTTP_201_CREATED)

    def _email(self, request, username, new_resource, reason):
        """
        Processes resource request increases. Sends email to atmo@iplantc.org

        Returns a response.
        """
        return resource_request_email(request, username, new_resource, reason)


class SupportEmail(AuthAPIView):

    def post(self, request):
        """
        Creates a new support email and sends it to admins.

        Post Support Email via RESTful API
        """
        required = ["message", "subject","user-interface"]
        missing_keys = check_missing_keys(request.DATA, required)
        if missing_keys:
            return keys_not_found(missing_keys)
        result = self._email(request,
                             request.DATA["subject"],
                             request.DATA["message"],
                             request.DATA)
        return Response(result, status=status.HTTP_201_CREATED)

    def _email(self, request, subject, message, data):
        """
        Sends an email to support.

        POST Params expected:
        * user
        * message
        * subject

        Returns a response.
        """
        data['server'] = settings.SERVER_URL
        email_success = email_admin(request, subject, message, data=data)
        return {"email_sent": email_success}


def check_missing_keys(data, required_keys):
    """
    Return any missing required post key names.
    """
    return [key for key in required_keys
            # Key must exist and have a non-empty value.
            if key not in data or
            (isinstance(data[key], str) and len(data[key]) > 0)]


def keys_not_found(missing_keys):
    return failure_response(
        status.HTTP_400_BAD_REQUEST,
        "Missing required POST data variables : %s" % missing_keys)
