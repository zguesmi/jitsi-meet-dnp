import docker
import logging
import os
import secrets
import string


# TODO: format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=os.getenv("LOG_LEVEL"))
log = logging.getLogger(__name__)

def exit_app():
    log.info("Exiting...")
    exit(1)

def generate_random_alphanumeric_string(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

class AppSecrets:
    def __init__(self):
        secret_length = 32
        self.jicofo_component_secret = generate_random_alphanumeric_string(secret_length)
        self.jicofo_auth_password = generate_random_alphanumeric_string(secret_length)
        self.jvb_auth_password = generate_random_alphanumeric_string(secret_length)
        self.jigasi_xmpp_password = generate_random_alphanumeric_string(secret_length)
        self.jibri_recorded_password = generate_random_alphanumeric_string(secret_length)
        self.jibri_xmpp_password = generate_random_alphanumeric_string(secret_length)


class ContainerConfig:
    def __init__(self, image, container_name, ports, volumes, network_aliases, restart_policy, env):
        self.image = image
        self.container_name = container_name
        self.ports = ports
        self.volumes = volumes
        # "network": self.docker_network,
        self.network_aliases = network_aliases
        self.restart_policy = restart_policy
        self.env = env


class AppConfig:
    def __init__(self):
        self.stack_version = os.getenv("STACK_VERSION")
        self.config_root_dir = os.getenv("CONFIG_ROOT_DIR")
        self.restart_policy = os.getenv("RESTART_POLICY")
        self.docker_network_name = os.getenv("DOCKER_NETWORK_NAME")
        self.secrets = AppSecrets()
        self.xmpp_container_config = ContainerConfig(
            image=f"jitsi/prosody:{self.stack_version}",
            container_name="jitsi-xmpp",
            ports={
                "5222": None,
                "5280": None,
                "5347": None,
            },
            volumes={
                f"{self.config_root_dir}/prosody/config": {
                    "bind": "/config",
                    "mode": "Z"
                },
                f"{self.config_root_dir}/prosody/prosody-plugins-custom": {
                    "bind": "/prosody-plugins-custom",
                    "mode": "Z"
                }
            },
            network_aliases=[os.getenv("XMPP_SERVER")],
            restart_policy={
                "Name": self.restart_policy,
                "MaximumRetryCount": 5
            },
            env={
                "AUTH_TYPE": os.getenv("AUTH_TYPE"),
                "ENABLE_AUTH": os.getenv("ENABLE_AUTH"),
                "ENABLE_GUESTS": os.getenv("ENABLE_GUESTS"),
                "GLOBAL_MODULES": os.getenv("GLOBAL_MODULES"),
                "GLOBAL_CONFIG": os.getenv("GLOBAL_CONFIG"),
                "LDAP_URL": os.getenv("LDAP_URL"),
                "LDAP_BASE": os.getenv("LDAP_BASE"),
                "LDAP_BINDDN": os.getenv("LDAP_BINDDN"),
                "LDAP_BINDPW": os.getenv("LDAP_BINDPW"),
                "LDAP_FILTER": os.getenv("LDAP_FILTER"),
                "LDAP_AUTH_METHOD": os.getenv("LDAP_AUTH_METHOD"),
                "LDAP_VERSION": os.getenv("LDAP_VERSION"),
                "LDAP_USE_TLS": os.getenv("LDAP_USE_TLS"),
                "LDAP_TLS_CIPHERS": os.getenv("LDAP_TLS_CIPHERS"),
                "LDAP_TLS_CHECK_PEER": os.getenv("LDAP_TLS_CHECK_PEER"),
                "LDAP_TLS_CACERT_FILE": os.getenv("LDAP_TLS_CACERT_FILE"),
                "LDAP_TLS_CACERT_DIR": os.getenv("LDAP_TLS_CACERT_DIR"),
                "LDAP_START_TLS": os.getenv("LDAP_START_TLS"),
                "XMPP_DOMAIN": os.getenv("XMPP_DOMAIN"),
                "XMPP_AUTH_DOMAIN": os.getenv("XMPP_AUTH_DOMAIN"),
                "XMPP_GUEST_DOMAIN": os.getenv("XMPP_GUEST_DOMAIN"),
                "XMPP_MUC_DOMAIN": os.getenv("XMPP_MUC_DOMAIN"),
                "XMPP_INTERNAL_MUC_DOMAIN": os.getenv("XMPP_INTERNAL_MUC_DOMAIN"),
                "XMPP_MODULES": os.getenv("XMPP_MODULES"),
                "XMPP_MUC_MODULES": os.getenv("XMPP_MUC_MODULES"),
                "XMPP_INTERNAL_MUC_MODULES": os.getenv("XMPP_INTERNAL_MUC_MODULES"),
                "XMPP_RECORDER_DOMAIN": os.getenv("XMPP_RECORDER_DOMAIN"),
                "JICOFO_COMPONENT_SECRET": self.secrets.jicofo_component_secret,
                "JICOFO_AUTH_USER": os.getenv("JICOFO_AUTH_USER"),
                "JICOFO_AUTH_PASSWORD": self.secrets.jicofo_auth_password,
                "JVB_AUTH_USER": os.getenv("JVB_AUTH_USER"),
                "JVB_AUTH_PASSWORD": self.secrets.jvb_auth_password,
                "JIGASI_XMPP_USER": os.getenv("JIGASI_XMPP_USER"),
                "JIGASI_XMPP_PASSWORD": self.secrets.jigasi_xmpp_password,
                "JIBRI_XMPP_USER": os.getenv("JIBRI_XMPP_USER"),
                "JIBRI_XMPP_PASSWORD": self.secrets.jibri_xmpp_password,
                "JIBRI_RECORDER_USER": os.getenv("JIBRI_RECORDER_USER"),
                "JIBRI_RECORDER_PASSWORD": self.secrets.jibri_recorded_password,
                "JWT_APP_ID": os.getenv("JWT_APP_ID"),
                "JWT_APP_SECRET": os.getenv("JWT_APP_SECRET"),
                "JWT_ACCEPTED_ISSUERS": os.getenv("JWT_ACCEPTED_ISSUERS"),
                "JWT_ACCEPTED_AUDIENCES": os.getenv("JWT_ACCEPTED_AUDIENCES"),
                "JWT_ASAP_KEYSERVER": os.getenv("JWT_ASAP_KEYSERVER"),
                "JWT_ALLOW_EMPTY": os.getenv("JWT_ALLOW_EMPTY"),
                "JWT_AUTH_TYPE": os.getenv("JWT_AUTH_TYPE"),
                "JWT_TOKEN_AUTH_MODULE": os.getenv("JWT_TOKEN_AUTH_MODULE"),
                "LOG_LEVEL": os.getenv("LOG_LEVEL"),
                "TZ": os.getenv("TZ")
            },
        )
        self.web_container_config = ContainerConfig(
            image=f"jitsi/web:{self.stack_version}",
            container_name="jitsi-web",
            ports={
                "80": int(os.getenv("HTTP_PORT")),
                "443": int(os.getenv("HTTPS_PORT"))
            },
            volumes={
                f"{self.config_root_dir}/web": {
                    "bind": "/config",
                    "mode": "Z"
                },
                f"{self.config_root_dir}/web/letsencrypt": {
                    "bind": "/etc/letsencrypt",
                    "mode": "Z"
                },
                f"{self.config_root_dir}/transcripts": {
                    "bind": "/usr/share/jitsi-meet/transcripts",
                    "mode": "Z"
                },
            },
            network_aliases=[os.getenv("XMPP_DOMAIN")],
            restart_policy={
                "Name": self.restart_policy,
                "MaximumRetryCount": 5
            },
            env={
                "ENABLE_AUTH": os.getenv("ENABLE_AUTH"),
                "ENABLE_GUESTS": os.getenv("ENABLE_GUESTS"),
                "ENABLE_LETSENCRYPT": "1" if os.getenv("ENABLE_LETSENCRYPT").lower == "true" else "",
                "ENABLE_HTTP_REDIRECT": os.getenv("ENABLE_HTTP_REDIRECT"),
                "ENABLE_TRANSCRIPTIONS": os.getenv("ENABLE_TRANSCRIPTIONS"),
                "DISABLE_HTTPS": os.getenv("DISABLE_HTTPS"),
                "JICOFO_AUTH_USER": os.getenv("JICOFO_AUTH_USER"),
                "LETSENCRYPT_DOMAIN": os.getenv("LETSENCRYPT_DOMAIN"),
                "LETSENCRYPT_EMAIL": os.getenv("LETSENCRYPT_EMAIL"),
                "PUBLIC_URL": os.getenv("PUBLIC_URL"),
                "XMPP_DOMAIN": os.getenv("XMPP_DOMAIN"),
                "XMPP_AUTH_DOMAIN": os.getenv("XMPP_AUTH_DOMAIN"),
                "XMPP_BOSH_URL_BASE": os.getenv("XMPP_BOSH_URL_BASE"),
                "XMPP_GUEST_DOMAIN": os.getenv("XMPP_GUEST_DOMAIN"),
                "XMPP_MUC_DOMAIN": os.getenv("XMPP_MUC_DOMAIN"),
                "XMPP_RECORDER_DOMAIN": os.getenv("XMPP_RECORDER_DOMAIN"),
                "ETHERPAD_URL_BASE": os.getenv("ETHERPAD_URL_BASE"),
                "TZ": os.getenv("TZ"),
                "JIBRI_BREWERY_MUC": os.getenv("JIBRI_BREWERY_MUC"),
                "JIBRI_PENDING_TIMEOUT": os.getenv("JIBRI_PENDING_TIMEOUT"),
                "JIBRI_XMPP_USER": os.getenv("JIBRI_XMPP_USER"),
                "JIBRI_XMPP_PASSWORD": self.secrets.jibri_xmpp_password,
                "JIBRI_RECORDER_USER": os.getenv("JIBRI_RECORDER_USER"),
                "JIBRI_RECORDER_PASSWORD": self.secrets.jibri_recorded_password,
                "ENABLE_RECORDING": os.getenv("ENABLE_RECORDING")
            }
        )
        self.jicofo_container_config = ContainerConfig(
            image=f"jitsi/jicofo:{self.stack_version}",
            container_name="jitsi-jicofo",
            ports={},
            volumes={
                f"{self.config_root_dir}/jicofo": {
                    "bind": "/config",
                    "mode": "Z"
                },
            },
            network_aliases=[],
            restart_policy={
                "Name": self.restart_policy,
                "MaximumRetryCount": 5
            },
            env={
                "AUTH_TYPE": os.getenv("AUTH_TYPE"),
                "ENABLE_AUTH": os.getenv("ENABLE_AUTH"),
                "XMPP_DOMAIN": os.getenv("XMPP_DOMAIN"),
                "XMPP_AUTH_DOMAIN": os.getenv("XMPP_AUTH_DOMAIN"),
                "XMPP_INTERNAL_MUC_DOMAIN": os.getenv("XMPP_INTERNAL_MUC_DOMAIN"),
                "XMPP_SERVER": os.getenv("XMPP_SERVER"),
                "JICOFO_COMPONENT_SECRET": self.secrets.jicofo_component_secret,
                "JICOFO_AUTH_USER": os.getenv("JICOFO_AUTH_USER"),
                "JICOFO_AUTH_PASSWORD": self.secrets.jicofo_auth_password,
                "JICOFO_RESERVATION_REST_BASE_URL": os.getenv("JICOFO_RESERVATION_REST_BASE_URL"),
                "JVB_BREWERY_MUC": os.getenv("JVB_BREWERY_MUC"),
                "JIGASI_BREWERY_MUC": os.getenv("JIGASI_BREWERY_MUC"),
                "JIGASI_SIP_URI": os.getenv("JIGASI_SIP_URI"),
                "JIBRI_BREWERY_MUC": os.getenv("JIBRI_BREWERY_MUC"),
                "JIBRI_PENDING_TIMEOUT": os.getenv("JIBRI_PENDING_TIMEOUT"),
                "TZ": os.getenv("TZ"),
            }
        )
        self.jvb_container_config = ContainerConfig(
            image=f"jitsi/jvb:{self.stack_version}",
            container_name="jitsi-jvb",
            ports={
                os.getenv("JVB_PORT") + "/udp": os.getenv("JVB_PORT"),
                os.getenv("JVB_TCP_PORT"): os.getenv("JVB_TCP_MAPPED_PORT")
            },
            volumes={
                f"{self.config_root_dir}/jvb": {
                    "bind": "/config",
                    "mode": "Z"
                },
            },
            network_aliases=[],
            restart_policy={
                "Name": self.restart_policy,
                "MaximumRetryCount": 5
            },
            env={
                "DOCKER_HOST_ADDRESS": os.getenv("DOCKER_HOST_ADDRESS"),
                "XMPP_AUTH_DOMAIN": os.getenv("XMPP_AUTH_DOMAIN"),
                "XMPP_INTERNAL_MUC_DOMAIN": os.getenv("XMPP_INTERNAL_MUC_DOMAIN"),
                "XMPP_SERVER": os.getenv("XMPP_SERVER"),
                "JVB_AUTH_USER": os.getenv("JVB_AUTH_USER"),
                "JVB_AUTH_PASSWORD": self.secrets.jvb_auth_password,
                "JVB_BREWERY_MUC": os.getenv("JVB_BREWERY_MUC"),
                "JVB_PORT": os.getenv("JVB_PORT"),
                "JVB_TCP_HARVESTER_DISABLED": os.getenv("JVB_TCP_HARVESTER_DISABLED"),
                "JVB_TCP_PORT": os.getenv("JVB_TCP_PORT"),
                "JVB_STUN_SERVERS": os.getenv("JVB_STUN_SERVERS"),
                "JVB_ENABLE_APIS": os.getenv("JVB_ENABLE_APIS"),
                "TZ": os.getenv("TZ")
            }
        )


class DockerHelper:

    docker_client = docker.from_env()

    @staticmethod
    def get_version():
        return DockerHelper.docker_client.version()["Version"]

    @staticmethod
    def remove_container_if_present(container_name):
        try:
            container = DockerHelper.docker_client.containers.get(container_name)
            log.info(f"Removing existing container [name:{container_name}]")
            container.remove(v=True, force=True)
        except:
            pass

    @staticmethod
    def create_container(container_config):
        try:
            container = DockerHelper.docker_client.containers.create(
                container_config.image,
                name=container_config.container_name,
                environment=container_config.env,
                ports=container_config.ports,
                volumes=container_config.volumes,
                restart_policy=container_config.restart_policy,
            )
            log.debug(f"Created container [name:{container.name}, id:{container.id}]")
            return container
        except Exception as e:
            log.error(f"Error creating container [name:{container_config.container_name}]")
            log.error(e)
            return None

    @staticmethod
    def create_network(network_name):
        try:
            existing_network = DockerHelper.docker_client.networks.get(network_name)
            log.debug(f"Docker network already exists [name:{existing_network.name}]")
            return existing_network
        except docker.errors.NotFound as e:
            log.info(f"Creating docker network [name:{network_name}]")
            return DockerHelper.docker_client.networks.create(network_name, driver="bridge")
        except Exception as e:
            log.error(f"Error creating docker network [name:{network_name}]")
            log.error(e)
            return None

    @staticmethod
    def pull_image(image_uri):
        try:
            log.info(f"Pulling image [uri:{image_uri}]")
            image = DockerHelper.docker_client.images.pull(image_uri)
            log.debug(f"Pulled image [uri:{image_uri}]")
            return image
        except Exception as e:
            log.error(f"Error pulling image [uri:{image_uri}]")
            log.error(e)
            return None
