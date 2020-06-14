import logging
import os
import secrets
import string


# TODO: format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def generate_random_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(32))

jicofo_component_secret = generate_random_password()
log.info("jicofo_component_secret: " + jicofo_component_secret)
jicofo_auth_password = generate_random_password()
log.info("jicofo_auth_password: " + jicofo_auth_password)
jvb_auth_password = generate_random_password()
log.info("jvb_auth_password: " + jvb_auth_password)
jigasi_xmpp_password = generate_random_password()
log.info("jigasi_xmpp_password: " + jigasi_xmpp_password)
jibri_recorded_password = generate_random_password()
log.info("jibri_recorded_password: " + jibri_recorded_password)
jibri_xmpp_password = generate_random_password()
log.info("jibri_xmpp_password: " + jibri_xmpp_password)

prosody = {
    "AUTH_TYPE" : os.getenv("AUTH_TYPE"),
    "ENABLE_AUTH" : os.getenv("ENABLE_AUTH"),
    "ENABLE_GUESTS" : os.getenv("ENABLE_GUESTS"),
    "GLOBAL_MODULES" : os.getenv("GLOBAL_MODULES"),
    "GLOBAL_CONFIG" : os.getenv("GLOBAL_CONFIG"),
    "LDAP_URL" : os.getenv("LDAP_URL"),
    "LDAP_BASE" : os.getenv("LDAP_BASE"),
    "LDAP_BINDDN" : os.getenv("LDAP_BINDDN"),
    "LDAP_BINDPW" : os.getenv("LDAP_BINDPW"),
    "LDAP_FILTER" : os.getenv("LDAP_FILTER"),
    "LDAP_AUTH_METHOD" : os.getenv("LDAP_AUTH_METHOD"),
    "LDAP_VERSION" : os.getenv("LDAP_VERSION"),
    "LDAP_USE_TLS" : os.getenv("LDAP_USE_TLS"),
    "LDAP_TLS_CIPHERS" : os.getenv("LDAP_TLS_CIPHERS"),
    "LDAP_TLS_CHECK_PEER" : os.getenv("LDAP_TLS_CHECK_PEER"),
    "LDAP_TLS_CACERT_FILE" : os.getenv("LDAP_TLS_CACERT_FILE"),
    "LDAP_TLS_CACERT_DIR" : os.getenv("LDAP_TLS_CACERT_DIR"),
    "LDAP_START_TLS" : os.getenv("LDAP_START_TLS"),
    "XMPP_DOMAIN" : os.getenv("XMPP_DOMAIN"),
    "XMPP_AUTH_DOMAIN" : os.getenv("XMPP_AUTH_DOMAIN"),
    "XMPP_GUEST_DOMAIN" : os.getenv("XMPP_GUEST_DOMAIN"),
    "XMPP_MUC_DOMAIN" : os.getenv("XMPP_MUC_DOMAIN"),
    "XMPP_INTERNAL_MUC_DOMAIN" : os.getenv("XMPP_INTERNAL_MUC_DOMAIN"),
    "XMPP_MODULES" : os.getenv("XMPP_MODULES"),
    "XMPP_MUC_MODULES" : os.getenv("XMPP_MUC_MODULES"),
    "XMPP_INTERNAL_MUC_MODULES" : os.getenv("XMPP_INTERNAL_MUC_MODULES"),
    "XMPP_RECORDER_DOMAIN" : os.getenv("XMPP_RECORDER_DOMAIN"),
    "JICOFO_COMPONENT_SECRET" : jicofo_component_secret,
    "JICOFO_AUTH_USER" : os.getenv("JICOFO_AUTH_USER"),
    "JICOFO_AUTH_PASSWORD" : jicofo_auth_password,
    "JVB_AUTH_USER" : os.getenv("JVB_AUTH_USER"),
    "JVB_AUTH_PASSWORD" : jvb_auth_password,
    "JIGASI_XMPP_USER" : os.getenv("JIGASI_XMPP_USER"),
    "JIGASI_XMPP_PASSWORD" : jigasi_xmpp_password,
    "JIBRI_XMPP_USER" : os.getenv("JIBRI_XMPP_USER"),
    "JIBRI_XMPP_PASSWORD" : jibri_xmpp_password,
    "JIBRI_RECORDER_USER" : os.getenv("JIBRI_RECORDER_USER"),
    "JIBRI_RECORDER_PASSWORD" : jibri_recorded_password,
    "JWT_APP_ID" : os.getenv("JWT_APP_ID"),
    "JWT_APP_SECRET" : os.getenv("JWT_APP_SECRET"),
    "JWT_ACCEPTED_ISSUERS" : os.getenv("JWT_ACCEPTED_ISSUERS"),
    "JWT_ACCEPTED_AUDIENCES" : os.getenv("JWT_ACCEPTED_AUDIENCES"),
    "JWT_ASAP_KEYSERVER" : os.getenv("JWT_ASAP_KEYSERVER"),
    "JWT_ALLOW_EMPTY" : os.getenv("JWT_ALLOW_EMPTY"),
    "JWT_AUTH_TYPE" : os.getenv("JWT_AUTH_TYPE"),
    "JWT_TOKEN_AUTH_MODULE" : os.getenv("JWT_TOKEN_AUTH_MODULE"),
    "LOG_LEVEL" : os.getenv("LOG_LEVEL"),
    "TZ" : os.getenv("TZ")
}

web = {
    "ENABLE_AUTH" : os.getenv("ENABLE_AUTH"),
    "ENABLE_GUESTS" : os.getenv("ENABLE_GUESTS"),
    "ENABLE_LETSENCRYPT" : os.getenv("ENABLE_LETSENCRYPT"),
    "ENABLE_HTTP_REDIRECT" : os.getenv("ENABLE_HTTP_REDIRECT"),
    "ENABLE_TRANSCRIPTIONS" : os.getenv("ENABLE_TRANSCRIPTIONS"),
    "DISABLE_HTTPS" : os.getenv("DISABLE_HTTPS"),
    "JICOFO_AUTH_USER" : os.getenv("JICOFO_AUTH_USER"),
    "LETSENCRYPT_DOMAIN" : os.getenv("LETSENCRYPT_DOMAIN"),
    "LETSENCRYPT_EMAIL" : os.getenv("LETSENCRYPT_EMAIL"),
    "PUBLIC_URL" : os.getenv("PUBLIC_URL"),
    "XMPP_DOMAIN" : os.getenv("XMPP_DOMAIN"),
    "XMPP_AUTH_DOMAIN" : os.getenv("XMPP_AUTH_DOMAIN"),
    "XMPP_BOSH_URL_BASE" : os.getenv("XMPP_BOSH_URL_BASE"),
    "XMPP_GUEST_DOMAIN" : os.getenv("XMPP_GUEST_DOMAIN"),
    "XMPP_MUC_DOMAIN" : os.getenv("XMPP_MUC_DOMAIN"),
    "XMPP_RECORDER_DOMAIN" : os.getenv("XMPP_RECORDER_DOMAIN"),
    "ETHERPAD_URL_BASE" : os.getenv("ETHERPAD_URL_BASE"),
    "TZ" : os.getenv("TZ"),
    "JIBRI_BREWERY_MUC" : os.getenv("JIBRI_BREWERY_MUC"),
    "JIBRI_PENDING_TIMEOUT" : os.getenv("JIBRI_PENDING_TIMEOUT"),
    "JIBRI_XMPP_USER" : os.getenv("JIBRI_XMPP_USER"),
    "JIBRI_XMPP_PASSWORD" : jibri_xmpp_password,
    "JIBRI_RECORDER_USER" : os.getenv("JIBRI_RECORDER_USER"),
    "JIBRI_RECORDER_PASSWORD" : jibri_recorded_password,
    "ENABLE_RECORDING" : os.getenv("ENABLE_RECORDING")
}

jicofo = {
    "AUTH_TYPE" : os.getenv("AUTH_TYPE"),
    "ENABLE_AUTH" : os.getenv("ENABLE_AUTH"),
    "XMPP_DOMAIN" : os.getenv("XMPP_DOMAIN"),
    "XMPP_AUTH_DOMAIN" : os.getenv("XMPP_AUTH_DOMAIN"),
    "XMPP_INTERNAL_MUC_DOMAIN" : os.getenv("XMPP_INTERNAL_MUC_DOMAIN"),
    "XMPP_SERVER" : os.getenv("XMPP_SERVER"),
    "JICOFO_COMPONENT_SECRET" : jicofo_component_secret,
    "JICOFO_AUTH_USER" : os.getenv("JICOFO_AUTH_USER"),
    "JICOFO_AUTH_PASSWORD" : jicofo_auth_password,
    "JICOFO_RESERVATION_REST_BASE_URL" : os.getenv("JICOFO_RESERVATION_REST_BASE_URL"),
    "JVB_BREWERY_MUC" : os.getenv("JVB_BREWERY_MUC"),
    "JIGASI_BREWERY_MUC" : os.getenv("JIGASI_BREWERY_MUC"),
    "JIGASI_SIP_URI" : os.getenv("JIGASI_SIP_URI"),
    "JIBRI_BREWERY_MUC" : os.getenv("JIBRI_BREWERY_MUC"),
    "JIBRI_PENDING_TIMEOUT" : os.getenv("JIBRI_PENDING_TIMEOUT"),
    "TZ" : os.getenv("TZ"),
}

jvb = {
    "DOCKER_HOST_ADDRESS" : os.getenv("DOCKER_HOST_ADDRESS"),
    "XMPP_AUTH_DOMAIN" : os.getenv("XMPP_AUTH_DOMAIN"),
    "XMPP_INTERNAL_MUC_DOMAIN" : os.getenv("XMPP_INTERNAL_MUC_DOMAIN"),
    "XMPP_SERVER" : os.getenv("XMPP_SERVER"),
    "JVB_AUTH_USER" : os.getenv("JVB_AUTH_USER"),
    "JVB_AUTH_PASSWORD" : jvb_auth_password,
    "JVB_BREWERY_MUC" : os.getenv("JVB_BREWERY_MUC"),
    "JVB_PORT" : os.getenv("JVB_PORT"),
    "JVB_TCP_HARVESTER_DISABLED" : os.getenv("JVB_TCP_HARVESTER_DISABLED"),
    "JVB_TCP_PORT" : os.getenv("JVB_TCP_PORT"),
    "JVB_STUN_SERVERS" : os.getenv("JVB_STUN_SERVERS"),
    "JVB_ENABLE_APIS" : os.getenv("JVB_ENABLE_APIS"),
    "TZ" : os.getenv("TZ")
}
