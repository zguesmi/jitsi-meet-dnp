import logging
import os
import docker
import signal
import time
import env


# TODO: format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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
            container = self.docker_client.containers.run(
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
                    .format(self.container_name, container.id))
            return container
        except Exception as e:
            log.error("Error running container [container_name:{}]".format(self.container_name))
            log.error(e)
            return None


class Jitsi():

    docker_network = None
    prosody_container = None
    web_container = None
    jicofo_container = None
    jvb_container = None

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

    def create_config_tree(self):
        log.info("Creating config tree [root_dir:{}]".format(self.config_root_dir))
        os.makedirs(self.config_root_dir + "/web/letsencrypt", exist_ok=True)
        os.makedirs(self.config_root_dir + "/transcripts", exist_ok=True)
        os.makedirs(self.config_root_dir + "/prosody/config", exist_ok=True)
        os.makedirs(self.config_root_dir + "/prosody/prosody-plugins-custom", exist_ok=True)
        os.makedirs(self.config_root_dir + "/jicofo", exist_ok=True)
        os.makedirs(self.config_root_dir + "/jvb", exist_ok=True)
        os.makedirs(self.config_root_dir + "/jigasi", exist_ok=True)
        os.makedirs(self.config_root_dir + "/jibri", exist_ok=True)

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
        self.prosody_container = DockerService(
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
        ).remove_if_present(True).run()
        self.docker_network.connect(container=self.prosody_container, aliases=[self.xmpp_server])

    """
    Jitsi web component.
    """
    def start_web_component(self):
        self.web_container = DockerService(
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
        ).remove_if_present(True).run()
        self.docker_network.connect(container=self.web_container, aliases=[self.internal_xmpp_domain])

    """
    Jitsi focus component.
    """
    def start_focus_component(self):
        self.jicofo_container = DockerService(
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
        ).remove_if_present(True).run()
        self.docker_network.connect(container=self.jicofo_container)

    """
    Jitsi video bridge component.
    """
    def start_video_bridge(self):
        self.jvb_container = DockerService(
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
        ).remove_if_present(True).run()
        self.docker_network.connect(container=self.jvb_container)

    def wait_services(self):
        self.prosody_container.wait()

if __name__ == "__main__":
    jitsi = Jitsi()
    jitsi.create_config_tree()
    jitsi.create_docker_network()
    try:
        log.info("Running XMPP server (Prosody)")
        prosody_container = jitsi.start_xmpp_server()
        log.info("Running focus component service (Jicofo)")
        jicofo_container = jitsi.start_focus_component()
        log.info("Running video bridge service (Jvb)")
        jvb_container = jitsi.start_video_bridge()
        log.info("Running Web service")
        web_container = jitsi.start_web_component()
        log.info("All services are up")
        jitsi.wait_services()
    except Exception as e:
        log.error("Error in main thread")
        log.exception(e)
        exit(1)

# class GracefulKiller:
#   kill_now = False
#   def __init__(self):
#     signal.signal(signal.SIGTERM, self.purge_jitsi_containers)
#     signal.signal(signal.SIGKILL, self.purge_jitsi_containers)

#   def purge_jitsi_containers(self, signum, frame):
#     self.kill_now = True

# if __name__ == "__main__":
#   killer = GracefulKiller()
#   while not killer.kill_now:
#     time.sleep(1)
#     print("doing something in a loop ...")

#   print("End of the program. I was killed gracefully :)")
