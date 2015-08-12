from django.utils.timezone import datetime, timedelta
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import jwt
import re
import base64
import urllib
import requests

from atmosphere.settings import secrets
from atmosphere.settings.saml_settings import SAML_SETTINGS, SAML_IDP_OAUTH_URL, SAML_ENTITY_ID, SAML_SP_URL, SAML_SP_OAUTH_KEY, SAML_SP_OAUTH_SECRET, SAML_CERT_TEXT_RAW, SAML_KEY_TEXT
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
from threepio import logger


@csrf_exempt
def saml_sso_process_response(request):
    return onelogin_saml_sso(request)


def get_user_for_token(token):
    pass

#Based off saml2


# Based off of https://github.com/onelogin/python-saml

def prepare_django_request(request):
    return {
        'http_host': request.META['HTTP_HOST'],
        'script_name': request.META['PATH_INFO'],
        'server_port': request.META['SERVER_PORT'],
        'query_params': request.META['QUERY_STRING'],
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy()
    }

def init_saml_auth(req):
    auth = Saml2_Auth(req, SAML_SETTINGS)
    return auth


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


def saml_sso_logout(request, redirect_to=None):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    logout_url =auth.logout()
    return logout_url

def saml_sso_login(request, redirect_to=None):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    login_url = auth.login(redirect_to, force_authn=True)
    return HttpResponseRedirect(login_url)

def saml_sso_sp_metadata(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    saml_settings = auth.get_settings()
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)
    if len(errors) == 0:
        logger.info(metadata)
    else:
        error_str = "Error(s) found on Metadata: %s"\
                    % (', '.join(errors))
        raise Exception(error_str)
    return HttpResponse(metadata)

def sign_assertion(assertion, key_data, cert):
    """
    TODO: Not sure if this method is required..
    """
    import xmlsec
    from lxml import etree
    root = etree.fromstring(assertion)

    signature_node = xmlsec.tree.find_node(root, xmlsec.Node.SIGNATURE)
    key = xmlsec.Key.from_memory(key_data, xmlsec.KeyFormat.PEM)

    sign_context = xmlsec.SignatureContext()
    sign_context.key = key
    sign_context.sign(signature_node)

    return etree.tostring(root)

def exchange_assertion_for_token(encoded_assertion):
    if not encoded_assertion:
        raise Exception("Why no assertion?")
    _assertion = base64.b64decode(encoded_assertion)
    logger.info(_assertion)
    signed_assertion = sign_assertion(_assertion, SAML_KEY_TEXT, SAML_CERT_TEXT_RAW)
    logger.info(signed_assertion)
    assertion = re.sub(r'\s', '', signed_assertion.encode('base64'))
    logger.info(assertion)
    token_request = {
            "grant_type":"urn:ietf:params:oauth:grant-type:saml2-bearer",
            "assertion": assertion,
            "client_id": SAML_SP_OAUTH_KEY,
            "scope": "PRODUCTION"
            }
    auth_key = base64.b64encode("%s:%s" % (SAML_SP_OAUTH_KEY, SAML_SP_OAUTH_SECRET))
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'Authorization': 'Basic %s' % auth_key}
    response = requests.post(
        SAML_IDP_OAUTH_URL, token_request, headers=headers,
        verify=False)
    response.raise_for_status()
    json_obj = response.json()
    return HttpResponse(json_obj)

def saml_sso_acs_response(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    response = auth.process_response()
    errors = auth.get_errors()
    if errors:
        raise Exception(
                "Error when processing ACS: %s" % (', '.join(errors)))
    if not auth.is_authenticated():
        logger.info('Not authenticated')
        return HttpResponse("Not Authenticated")
    raw_saml_response = auth._OneLogin_Saml2_Auth__request_data['post_data']['SAMLResponse']
    return exchange_assertion_for_token(raw_saml_response)
    #TODO: attributes are empty
    request.session['samlUserdata'] = auth.get_attributes()
    request.session['samlUsername'] = auth.get_nameid()
    if 'RelayState' in req['post_data'] and \
      Saml2_Utils.get_self_url(req) != req['post_data']['RelayState']:
        redirect_url = auth.redirect_to(req['post_data']['RelayState'])
        logger.info("Redirecting to 'RelayState'=%s" % redirect_url)
        return HttpResponseRedirect(redirect_url)
    else:
        for attr_name in request.session['samlUserdata'].keys():
            logger.info('%s ==> %s' % (attr_name, '|| '.join(request.session['samlUserdata'][attr_name])))
        return HttpResponse("SSO worked!")

@csrf_exempt
def onelogin_saml_sso(request):
    #logger.info("Incoming request to the SAML SSO endpoint: %s" % request.__dict__)
    query_params = request.META['QUERY_STRING']
    if 'sso' in query_params:                   # SSO action (SP-SSO initited).  Will send an AuthNRequest to the IdP
        return saml_sso_login(request)
    elif 'acs' in query_params or request.POST:             # Assertion Consumer Service invoked
        return saml_sso_acs_response(request)
    elif 'slo' in query_params:                     # SLO action. Will sent a Logout Request to IdP
        return saml_sso_logout(request)
    elif 'sls' in query_params:                                             # Single Logout Service
        return saml_sso_process_logout_response(request)
    elif 'samlUserdata' in request.session:
        return HttpResponse("You have an active session - %s - %s" % (request.session['samlUsername'], request.session['samlUserdata']))
    else:
        return HttpResponse("No Action detected based on query-params: %s" % query_params)
