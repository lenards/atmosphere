import base64
import sys
from onelogin.saml2.settings import OneLogin_Saml2_Settings as Saml2_Settings

globals().update(vars(sys.modules['atmosphere.settings']))

SAML_SETTINGS = {
    "strict": False,
    "debug": True,
    "sp": {
        "entityId": SAML_ENTITY_ID,
        "assertionConsumerService": {
            "url": SAML_SP_URL,
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
        },
        "singleLogoutService": {
            "url": SAML_SP_URL+ "/?sls",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "NameIDFormat": "urn:oasis:names:tc:SAML:2.0:nameid-format:unspecified",
        "x509cert": SAML_CERT_TEXT,
        "privateKey": SAML_KEY_TEXT,
    },
    "idp": {
        "entityId": SAML_IDP_URL + "/samlsso/",
        "singleSignOnService": {
            "url": SAML_IDP_URL + "/samlsso/",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "singleLogoutService": {
            "url": SAML_IDP_URL + "/samlsso/",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "x509cert": SAML_IDP_CERT,
    }
}
SAML_ADVANCED_SETTINGS = {
    # Security settings
    "security": {

        ##* signatures and encryptions offered **/

        # Indicates that the nameID of the <samlp:logoutRequest> sent by this SP
        # will be encrypted.
        "nameIdEncrypted": False,

        # Indicates whether the <samlp:AuthnRequest> messages sent by this SP
        # will be signed.  [Metadata of the SP will offer this info]
        "authnRequestsSigned": True,

        # Indicates whether the <samlp:logoutRequest> messages sent by this SP
        # will be signed.
        "logoutRequestSigned": False,

        # Indicates whether the <samlp:logoutResponse> messages sent by this SP
        # will be signed.
        "logoutResponseSigned": False,

        ## Sign the Metadata
        # False || True (use sp certs) || {
        #                                    "keyFileName": "metadata.key",
        #                                    "certFileName": "metadata.crt"
        #                                 }
        #
        "signMetadata": False,
        # signatures and encryptions required

        # Indicates a requirement for the <samlp:Response>, <samlp:LogoutRequest>
        # and <samlp:LogoutResponse> elements received by this SP to be signed.
        "wantMessagesSigned": False,

        # Indicates a requirement for the <saml:Assertion> elements received by
        # this SP to be signed. [Metadata of the SP will offer this info]
        "wantAssertionsSigned": False,

        # Indicates a requirement for the NameID received by
        # this SP to be encrypted.
        "wantNameIdEncrypted": False
    },
    # Contact information template, it is recommended to suply a
    # technical and support contacts.
    "contactPerson": {
        "technical": {
            "givenName": "technical_name",
            "emailAddress": "technical@example.com"
        },
        "support": {
            "givenName": "support_name",
            "emailAddress": "support@example.com"
        }
    },
    # Organization information template, the info in en_US lang is
    # recomended, add more if required.
    "organization": {
        "en-US": {
            "name": "sp_test",
            "displayname": "SP test",
            "url": "http://sp.example.com"
        }
    }
}
SAML_SETTINGS.update(SAML_ADVANCED_SETTINGS)
SSO_SAML_SETTINGS = Saml2_Settings(SAML_SETTINGS)
