from django.utils.timezone import datetime, timedelta
from django.http import HttpResponseRedirect, HttpResponse

import jwt
import requests

from atmosphere.settings import secrets
from atmosphere.settings import SAML_SETTINGS
from atmosphere import settings
from authentication import get_or_create_user
from authentication.models import Token as AuthToken
from core.models.user import AtmosphereUser

from onelogin.saml2.auth import \
    OneLogin_Saml2_Auth as Saml2_Auth
from onelogin.saml2.settings import \
    OneLogin_Saml2_Settings as Saml2_Settings
from onelogin.saml2.utils import \
    OneLogin_Saml2_Utils as Saml2_Utils
from threepio import auth_logger as logger

# Based off of https://github.com/onelogin/python-saml

def prepare_from_django_request(request):
    return {
        'http_host': request.META['HTTP_HOST'],
        'script_name': request.META['PATH_INFO'],
        'server_port': request.META['SERVER_PORT'],
        'query_params': request.META['QUERY_STRING'],
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy()
    }

def get_user_for_token(token):
    pass

def saml_sso_process_logout_response(request):
    delete_session_callback = lambda: request.session.flush()
    url = auth.process_slo(delete_session_cb=delete_session_callback)
    errors = auth.get_errors()
    if len(errors) == 0:
        if url is not None:
            return HttpResponseRedirect(url)
        else:
            logger.info("Sucessfully Logged out")
            return HttpResponseRedirect('/logout')
    else:
        raise Exception(
                "Error when processing SLO: %s" % (', '.join(errors)))


def saml_sso_login_HttpResponseRedirect(request):
    req = prepare_from_django_request(request)
    auth = Saml2_Auth(req, SAML_SETTINGS)
    return auth.login() # Build and send AuthNRequest

def saml_sso_sp_metadata(request):
    saml_settings = auth.get_settings()
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)
    if len(errors) == 0:
        auth_logger.info(metadata)
    else:
        error_str = "Error(s) found on Metadata: %s"\
                    % (', '.join(errors))
        raise Exception(error_str)
    return metadata

def saml_sso_process_response(request):
    req = prepare_from_django_request(request)  # Process the request and build the request dict that
                                                # the toolkit expects

    auth = Saml2_Auth(req, SAML_SETTINGS)       # Initialize the SP SAML instance
    query_params = req['query_params']

    if 'sso' in query_params:                   # SSO action (SP-SSO initited).  Will send an AuthNRequest to the IdP
        return HttpResponseHttpResponseRedirect(auth.login())
    elif 'sso2' in query_params:                       # Another SSO init action
        return_to = '%sattrs/' % request.host_url      # but set a custom RelayState URL
        return HttpResponseRedirect(auth.login(return_to))
    elif 'slo' in query_params:                     # SLO action. Will sent a Logout Request to IdP
        return HttpResponseRedirect(auth.logout())
    elif 'acs' in query_params:                 # Assertion Consumer Service
        auth.process_response()                     # Process the Response of the IdP
        errors = auth.get_errors()              # This method receives an array with the errors
        if len(errors) == 0:                    # that could took place during the process
            if not auth.is_authenticated():         # This check if the response was ok and the user
                msg = "Not authenticated"           # data retrieved or not (user authenticated)
            else:
                request.session['samlUserdata'] = auth.get_attributes()     # Retrieves user data
                self_url = OneLogin_Saml2_Utils.get_self_url(req)
                if 'RelayState' in request.form and self_url != request.form['RelayState']:
                    return HttpResponseRedirect(auth.redirect_to(request.form['RelayState']))   # Redirect if there is a relayState
                else:                           # If there is user data we save that to print it later
                    msg = ''
                    for attr_name in request.session['samlUserdata'].keys():
                        msg += '%s ==> %s' % (attr_name, '|| '.join(request.session['samlUserdata'][attr_name]))
    elif 'sls' in query_params:                                             # Single Logout Service
        delete_session_callback = lambda: session.clear()           # Obtain session clear callback
        url = auth.process_slo(delete_session_cb=delete_session_callback)   # Process the Logout Request & Logout Response
        errors = auth.get_errors()              #  Retrieves possible validation errors
        if len(errors) == 0:
            if url is not None:
                return HttpResponseRedirect(url)
            else:
                msg = "Sucessfully logged out"
    return HttpResponse("No Action detected based on query-params: %s" % query_params)

def saml_sso_acs_response(request):
    req = prepare_from_django_request(request)
    auth = Saml2_Auth(req, SAML_SETTINGS)
    auth.process_response()
    errors = auth.get_errors()
    if not errors:
        if not auth.is_authenticated():
            request.session['samlUserdata'] = auth.get_attributes()
            if 'RelayState' in req['post_data'] and \
              Saml2_Utils.get_self_url(req) != req['post_data']['RelayState']:
                auth.redirect_to(req['post_data']['RelayState'])
            else:
                for attr_name in request.session['samlUserdata'].keys():
                    logger.info('%s ==> %s' % (attr_name, '|| '.join(request.session['samlUserdata'][attr_name])))
        else:
          logger.info('Not authenticated')
    else:
        logger.info("Error when processing SAML Response: %s" % (', '.join(errors)))
