"""
WSO2 authentication protocol

"""
from datetime import timedelta
import time

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from threepio import auth_logger as logger

from atmosphere import settings
from authentication import create_session_token
from authentication.models import UserProxy
from core.models import AtmosphereUser as User

# TODO: Find out the actual proxy ticket expiration time, it varies by server
# May be as short as 5min!
PROXY_TICKET_EXPIRY = timedelta(days=1)


#def wso2_revalidation(username):
#    """
#    Because this is a programmatic request
#    and CAS requires user input when expired,
#    We MUST use CAS Proxy Service,
#    and see if we can reauthenticate the user.
#    """
#    try:
#        userProxy = UserProxy.objects.filter(username=username).latest('pk')
#        logger.debug("[CAS] Validation Test - %s" % username)
#        if userProxy is None:
#            logger.debug("User %s does not have a proxy" % username)
#            return (False, None)
#        proxyTicket = userProxy.proxyTicket
#        caslib = get_cas_client()
#        (validUser, cas_response) =\
#            caslib.reauthenticate(proxyTicket, username=username)
#        logger.debug("Valid User: %s Proxy response: %s"
#                     % (validUser, cas_response))
#        return (validUser, cas_response)
#    except Exception:
#        logger.exception('Error validating user %s' % username)
#        return (False, None)
def saml_ssl_service(request):
    if request.method != 'POST':
        return HttpResponse("I expected a SAML Post to be coming here!")
    return validate_saml(request)


def to_identity_server(request):
    identity_server_url = "https://52.3.10.15:9563/publisher"
    issuer_id="atmomickey"
    callback= "https://mickey.iplantc.org/auth/ws02"
    saml_response = SAMLResponse()
    return HttpResponseRedirect(identity_server_url, saml_response)


def validate_saml(request):
    """
    The web application receives the POST request, processes the SAML message for the user’s identity information (e.g. username).
    If necessary, the application makes a POST request to the OAuth token endpoint passing the SAML assertion as the authorization grant and passing a grant_type of 
    ``urn:ietf:params:oauth:grant-type:saml2-bearer``
    The OAuth server responds with an access token.

    After a WS02 Login:
    Redirects the request to THIS url and sends a POST request
    We processrequest and exchange for an oauth token
    OAuth server gives access token, which is saved for API use.
    """
    logger.debug('POST Variables:%s' % request.POST)


def validate_token(access_token):
    """
    AFTER going through the 'wso2 dance' above, user has an AccessToken.

    They passed the AccessToken for API access and it must be validated w/ the wso2 server.
    """
    return False
