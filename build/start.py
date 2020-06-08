import sys
import os
import docker


version = "stable-4548"

web = {
    "image": "jitsi/web:" + version,
    "env": {
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
        "JIBRI_XMPP_PASSWORD" : os.getenv("JIBRI_XMPP_PASSWORD"),
        "JIBRI_RECORDER_USER" : os.getenv("JIBRI_RECORDER_USER"),
        "JIBRI_RECORDER_PASSWORD" : os.getenv("JIBRI_RECORDER_PASSWORD"),
        "ENABLE_RECORDING" : os.getenv("ENABLE_RECORDING")
    }
}
prosody = {
    "image": "jitsi/prosody:" + version,
    "env": {
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
        "JICOFO_COMPONENT_SECRET" : os.getenv("JICOFO_COMPONENT_SECRET"),
        "JICOFO_AUTH_USER" : os.getenv("JICOFO_AUTH_USER"),
        "JICOFO_AUTH_PASSWORD" : os.getenv("JICOFO_AUTH_PASSWORD"),
        "JVB_AUTH_USER" : os.getenv("JVB_AUTH_USER"),
        "JVB_AUTH_PASSWORD" : os.getenv("JVB_AUTH_PASSWORD"),
        "JIGASI_XMPP_USER" : os.getenv("JIGASI_XMPP_USER"),
        "JIGASI_XMPP_PASSWORD" : os.getenv("JIGASI_XMPP_PASSWORD"),
        "JIBRI_XMPP_USER" : os.getenv("JIBRI_XMPP_USER"),
        "JIBRI_XMPP_PASSWORD" : os.getenv("JIBRI_XMPP_PASSWORD"),
        "JIBRI_RECORDER_USER" : os.getenv("JIBRI_RECORDER_USER"),
        "JIBRI_RECORDER_PASSWORD" : os.getenv("JIBRI_RECORDER_PASSWORD"),
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
}

jicofo = {
    "image": "jitsi/jicofo:" + version,
    "env": {
        "AUTH_TYPE" : os.getenv("AUTH_TYPE"),
        "ENABLE_AUTH" : os.getenv("ENABLE_AUTH"),
        "XMPP_DOMAIN" : os.getenv("XMPP_DOMAIN"),
        "XMPP_AUTH_DOMAIN" : os.getenv("XMPP_AUTH_DOMAIN"),
        "XMPP_INTERNAL_MUC_DOMAIN" : os.getenv("XMPP_INTERNAL_MUC_DOMAIN"),
        "XMPP_SERVER" : os.getenv("XMPP_SERVER"),
        "JICOFO_COMPONENT_SECRET" : os.getenv("JICOFO_COMPONENT_SECRET"),
        "JICOFO_AUTH_USER" : os.getenv("JICOFO_AUTH_USER"),
        "JICOFO_AUTH_PASSWORD" : os.getenv("JICOFO_AUTH_PASSWORD"),
        "JICOFO_RESERVATION_REST_BASE_URL" : os.getenv("JICOFO_RESERVATION_REST_BASE_URL"),
        "JVB_BREWERY_MUC" : os.getenv("JVB_BREWERY_MUC"),
        "JIGASI_BREWERY_MUC" : os.getenv("JIGASI_BREWERY_MUC"),
        "JIGASI_SIP_URI" : os.getenv("JIGASI_SIP_URI"),
        "JIBRI_BREWERY_MUC" : os.getenv("JIBRI_BREWERY_MUC"),
        "JIBRI_PENDING_TIMEOUT" : os.getenv("JIBRI_PENDING_TIMEOUT"),
        "TZ" : os.getenv("TZ"),
    }
}

jvb = {
    "name": "jitsi/jvb:" + version,
    "env": {
        "DOCKER_HOST_ADDRESS" : os.getenv("DOCKER_HOST_ADDRESS"),
        "XMPP_AUTH_DOMAIN" : os.getenv("XMPP_AUTH_DOMAIN"),
        "XMPP_INTERNAL_MUC_DOMAIN" : os.getenv("XMPP_INTERNAL_MUC_DOMAIN"),
        "XMPP_SERVER" : os.getenv("XMPP_SERVER"),
        "JVB_AUTH_USER" : os.getenv("JVB_AUTH_USER"),
        "JVB_AUTH_PASSWORD" : os.getenv("JVB_AUTH_PASSWORD"),
        "JVB_BREWERY_MUC" : os.getenv("JVB_BREWERY_MUC"),
        "JVB_PORT" : os.getenv("JVB_PORT"),
        "JVB_TCP_HARVESTER_DISABLED" : os.getenv("JVB_TCP_HARVESTER_DISABLED"),
        "JVB_TCP_PORT" : os.getenv("JVB_TCP_PORT"),
        "JVB_STUN_SERVERS" : os.getenv("JVB_STUN_SERVERS"),
        "JVB_ENABLE_APIS" : os.getenv("JVB_ENABLE_APIS"),
        "TZ" : os.getenv("TZ")
    }
}

client = docker.from_env()
# container = client.containers.run("ubuntu:18.04", detach=True)
# print(container.id)
# for image in client.images.list():
#     print(image)


class jitsi_web():
    def __init__(self):
        self.image = "jitsi/web:" + version
        self.env = web.get('env')
        self.ports = {
            os.getenv("HTTP_PORT"):80,
            os.getenv("HTTPS_PORT"):443
        }
        self.volumes = {
            '${CONFIG}/web': {
                'bind': '/mnt/vol2',
                'mode': 'rw'
            },
            '/var/www': {
                'bind': '/mnt/vol1',
                'mode': 'ro'
            }
        }
    #   - ${CONFIG}/web:/config:Z
    #   - ${CONFIG}/web/letsencrypt:/etc/letsencrypt:Z
    #   - ${CONFIG}/transcripts:/usr/share/jitsi-meet/transcripts:Z
    # networks:
    #   meet.jitsi:
    #     aliases:
    #       - ${XMPP_DOMAIN}



# web_container = client.containers.create(web_image)
# web_container.

container = client.containers.run(web_image, environment=env , detach=True)




















# import os
# path = '/home/dail/first/second/third'
# os.makedirs(path, exist_ok=True)

# ~/.jitsi-meet-cfg/web/letsencrypt
# ~/.jitsi-meet-cfg/transcripts
# ~/.jitsi-meet-cfg/prosody/config
# ~/.jitsi-meet-cfg/prosody/prosody-plugins-custom
# ~/.jitsi-meet-cfg/jicofo
# ~/.jitsi-meet-cfg/jvb
# ~/.jitsi-meet-cfg/jigasi
# ~/.jitsi-meet-cfg/jibri}