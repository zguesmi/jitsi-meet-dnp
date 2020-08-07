import logging
import os
import docker
import shutil
import signal
import time

import env


# TODO: format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class DockerService():

    container = None

    def __init__(self, docker_client, image, container_name, ports, volumes, env, restart_policy):
        self.docker_client = docker_client
        self.image = image
        self.container_name = container_name
        self.ports = ports
        self.volumes = volumes
        self.env = env
        self.restart_policy = restart_policy

    def remove_if_present(self, force):
        try:
            container = self.docker_client.containers.get(self.container_name)
            if container is not None:
                log.info("Removing existing container [container_name:{}, force:{}]".format(self.container_name, force))
                container.remove(v=True, force=force)
        finally:
            return self

    def run(self):
        try:
            self.container = self.docker_client.containers.run(
                self.image,
                name=self.container_name,
                environment=self.env,
                ports=self.ports,
                volumes=self.volumes,
                detach=True,
                restart_policy=self.restart_policy,
                remove=True
            )
            log.info("Started container [container_name:{}, container_id:{}]"
                    .format(self.container_name, self.container.id))
            return self.container
        except Exception as e:
            log.error("Error running container [container_name:{}]".format(self.container_name))
            log.error(e)
            return None


class Jitsi():

    docker_network = None
    xmpp_service = None
    web_component = None
    jicofo_service = None
    jvb_service = None

    def __init__(self):
        self.config_root_dir = os.getenv("CONFIG_ROOT_DIR")
        self.stack_version = os.getenv("STACK_VERSION")
        self.restart_policy = os.getenv("RESTART_POLICY")
        self.internal_xmpp_domain = os.getenv("XMPP_DOMAIN")
        self.xmpp_server_name = os.getenv("XMPP_SERVER")
        self.http_port = os.getenv("HTTP_PORT")
        self.https_port = os.getenv("HTTPS_PORT")
        self.docker_network_name = os.getenv("DOCKER_NETWORK_NAME")
        self.client = docker.from_env()
        signal.signal(signal.SIGINT, self.purge_containers)
        signal.signal(signal.SIGTERM, self.purge_containers)
        # signal.signal(signal.SIGKILL, self.purge_containers)

    def clean_config_tree(self):
        log.info("Cleaning possible residual config files [root_dir:{}]".format(self.config_root_dir))
        if os.path.exists(self.config_root_dir):
            for folder in os.listdir(self.config_root_dir):
                shutil.rmtree(os.path.join(self.config_root_dir, folder))

    def create_docker_network(self):
        try:
            self.docker_network = self.client.networks.get(self.docker_network_name)
            log.info("Docker network already exists [name:{}]".format(self.docker_network_name))
        except docker.errors.NotFound as e:
            log.info("Creating docker network [name:{}]".format(self.docker_network_name))
            self.docker_network = self.client.networks.create(self.docker_network_name, driver="bridge")
        except Exception as e:
            log.error("Error creating docker network [name:{}]".format(self.docker_network_name))
            log.error(e)
            exit(1)

    """
    Jitsi XMPP component (prosody).
    """
    def start_xmpp_server(self):
        self.xmpp_service = DockerService(
            docker_client=self.client,
            image="jitsi/prosody:" + self.stack_version,
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
                },
            },
            env=env.xmpp,
            restart_policy={
                "Name": self.restart_policy,
                "MaximumRetryCount": 5
            }
        )
        self.xmpp_service.remove_if_present(force=True)
        self.xmpp_service.run()
        self.docker_network.connect(container=self.xmpp_service.container, aliases=[self.xmpp_server_name])

    """
    Jitsi web component.
    """
    def start_web_component(self):
        self.web_component = DockerService(
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
        )
        self.web_component.remove_if_present(force=True)
        self.web_component.run()
        self.docker_network.connect(container=self.web_component.container, aliases=[self.internal_xmpp_domain])

    """
    Jitsi focus component.
    """
    def start_focus_component(self):
        self.jicofo_service = DockerService(
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
        )
        self.jicofo_service.remove_if_present(force=True)
        self.jicofo_service.run()
        self.docker_network.connect(container=self.jicofo_service.container)

    """
    Jitsi video bridge component.
    """
    def start_video_bridge(self):
        self.jvb_service = DockerService(
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
        )
        self.jvb_service.remove_if_present(force=True)
        self.jvb_service.run()
        self.docker_network.connect(container=self.jvb_service.container)

    def wait(self):
        self.xmpp_service.container.wait()

    def purge_containers(self):
        self.web_component.remove_if_present(force=True)
        self.jvb_service.remove_if_present(force=True)
        self.jicofo_service.remove_if_present(force=True)
        self.xmpp_service.remove_if_present(force=True)


if __name__ == "__main__":
    jitsi = Jitsi()
    jitsi.clean_config_tree()
    jitsi.create_docker_network()
    try:
        log.info("Running XMPP server (Prosody)")
        jitsi.start_xmpp_server()
        log.info("Running focus component (Jicofo)")
        jitsi.start_focus_component()
        log.info("Running video bridge (Jvb)")
        jitsi.start_video_bridge()
        log.info("Running web component")
        jitsi.start_web_component()
        log.info("All services are up")
        jitsi.wait()
    except Exception as e:
        jitsi.purge_containers()
        log.error("Error in main thread")
        log.exception(e)
        exit(1)
