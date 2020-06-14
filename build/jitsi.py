import logging
import os
import docker
import time

import env


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class DockerService():
    def __init__(self, docker_client, image, container_name, ports, volumes, env, restart_policy):
        self.docker_client = docker_client
        self.image = image
        self.container_name = container_name
        self.ports = ports
        self.volumes = volumes
        self.env = env
        self.restart_policy = restart_policy

    def run(self):
        return self.docker_client.containers.run(
            self.image,
            name=self.container_name,
            environment=self.env,
            ports=self.ports,
            volumes=self.volumes,
            detach=True,
            restart_policy=self.restart_policy,
            # remove=True
        )


class Jitsi():

    def __init__(self):
        self.config_root_dir = os.getenv("CONFIG_ROOT_DIR")
        self.stack_version = os.getenv("STACK_VERSION")
        self.restart_policy = os.getenv("RESTART_POLICY")
        self.internal_xmpp_domain = os.getenv("XMPP_DOMAIN")
        self.xmpp_server = os.getenv("XMPP_SERVER")
        self.http_port = os.getenv("HTTP_PORT")
        self.https_port = os.getenv("HTTPS_PORT")
        self.docker_network_name = os.getenv("DOCKER_NETWORK_NAME")
        self.client = docker.from_env()
        self.docker_network = None

    def create_docker_network(self):
        try:
            self.docker_network = self.client.networks.get(self.docker_network_name)
        except docker.errors.NotFound as e:
            self.docker_network = self.client.networks.create(self.docker_network_name, driver="bridge")
        except Exception as e:
            log.error('Error creating network: ' + self.docker_network_name)
            log.exception(e)
            exit(1)

    def create_config_tree(self):
        os.makedirs(self.config_root_dir + "/web/letsencrypt", exist_ok=True)
        os.makedirs(self.config_root_dir + "/transcripts", exist_ok=True)
        os.makedirs(self.config_root_dir + "/prosody/config", exist_ok=True)
        os.makedirs(self.config_root_dir + "/prosody/prosody-plugins-custom", exist_ok=True)
        os.makedirs(self.config_root_dir + "/jicofo", exist_ok=True)
        os.makedirs(self.config_root_dir + "/jvb", exist_ok=True)
        os.makedirs(self.config_root_dir + "/jigasi", exist_ok=True)
        os.makedirs(self.config_root_dir + "/jibri", exist_ok=True)

    """
    Jitsi prosody component.
    """
    def start_prosody(self):
        prosody_container = DockerService(
            docker_client=self.client,
            image="jitsi/prosody:" + self.stack_version,
            container_name="jitsi-prosody",
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
                },
            },
            env=env.prosody,
            restart_policy={
                "Name": self.restart_policy,
                "MaximumRetryCount": 5
            }
        ).run()
        self.docker_network.connect(container=prosody_container, aliases=[self.xmpp_server])
        return prosody_container

    """
    Jitsi web component.
    """
    def start_web_component(self):
        web_container = DockerService(
            docker_client=self.client,
            image="jitsi/web:" + self.stack_version,
            container_name="jitsi-web",
            ports={
                "80": int(self.http_port),
                "443": int(self.https_port)
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
            env=env.web,
            restart_policy={
                "Name": self.restart_policy,
                "MaximumRetryCount": 5
            }
        ).run()
        self.docker_network.connect(container=web_container, aliases=[self.internal_xmpp_domain])
        return web_container

    """
    Jitsi focus component.
    """
    def start_jifoco(self):
        jicofo_container = DockerService(
            docker_client=self.client,
            image="jitsi/jicofo:" + self.stack_version,
            container_name="jitsi-jicofo",
            ports={},
            volumes={
                f"{self.config_root_dir}/jicofo": {
                    "bind": "/config",
                    "mode": "Z"
                },
            },
            env=env.jicofo,
            restart_policy={
                "Name": self.restart_policy,
                "MaximumRetryCount": 5
            }
        ).run()
        self.docker_network.connect(container=jicofo_container)
        return jicofo_container

    """
    Jitsi video bridge component.
    """
    def start_jvb(self):
        jvb_container = DockerService(
            docker_client=self.client,
            image="jitsi/jvb:" + self.stack_version,
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
            env=env.jvb,
            restart_policy={
                "Name": self.restart_policy,
                "MaximumRetryCount": 5
            }
        ).run()
        self.docker_network.connect(container=jvb_container)
        return jvb_container

if __name__ == "__main__":
    jitsi = Jitsi()
    log.info("Creating config tree dirs")
    jitsi.create_config_tree()
    log.info("Creating docker network")
    jitsi.create_docker_network()
    log.info("Starting jitsi services")

    try:
        prosody_container = jitsi.start_prosody()
        log.info("Prosody container id: " + prosody_container.id)
        web_container = jitsi.start_web_component()
        log.info("Web container id: " + web_container.id)
        jicofo_container = jitsi.start_jifoco()
        log.info("Jicofo container id: " + jicofo_container.id)
        jvb_container = jitsi.start_jvb()
        log.info("Jvb container id: " + jvb_container.id)
        prosody_container.wait()
    except Exception as e:
        log.exception(e)
