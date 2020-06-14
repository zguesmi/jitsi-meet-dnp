import logging
import os
import docker
import jitsi
import time


class Jitsi_service():
    def __init(self, image, container_name, ports, volumes, env, network, restart_policy):
        self.image = image
        self.container_name = container_name
        self.ports = ports
        self.volumes = volumes
        self.env = env
        self.network = network
        self.restart_policy = restart_policy

        def run(self, client):
            return client.containers.run(
                self.image,
                name=self.container_name,
                environment=self.env,
                ports=self.ports,
                network=self.network,
                volumes=self.volumes,
                detach=True,
                # restart_policy=self.restart_policy,
                # remove=True
            )
            


class App():

    def __init(self):
        logging.basicConfig(level=logging.INFO)
        logging.info("### Start")
        self.config_root_dir = os.getenv("CONFIG_ROOT_DIR")
        self.docker_network_name = "meet.jitsi"
        self.client = docker.from_env()

    def create_docker_network(self):
        try:
            client.networks.get(self.docker_network_name)
        except docker.errors.NotFound as e:
            client.networks.create(self.docker_network_name, driver="bridge")
        except:
            print('Error creating network: ' + self.docker_network_name)
            exit()

    def create_config_tree(self):
        os.makedirs(self.config_root_dir + "/web/letsencrypt", exist_ok=True)
        os.makedirs(self.config_root_dir + "/transcripts", exist_ok=True)
        os.makedirs(self.config_root_dir + "/prosody/config", exist_ok=True)
        os.makedirs(self.config_root_dir + "/prosody/prosody-plugins-custom", exist_ok=True)
        os.makedirs(self.config_root_dir + "/jicofo", exist_ok=True)
        os.makedirs(self.config_root_dir + "/jvb", exist_ok=True)
        os.makedirs(self.config_root_dir + "/jigasi", exist_ok=True)
        os.makedirs(self.config_root_dir + "/jibri", exist_ok=True)

    def run(self):
        # should start prosody service first
        prosody = Jitsi_service(
            image="jitsi/prosody:" + stack_version,
            container_name="jitsi-prosody",
            ports={
                5222:5222,
                5347:5347,
                5280:5280
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
            env={},
            network=docker_network_name,
            restart_policy={
                "Name": os.getenv("RESTART_POLICY"),
                "MaximumRetryCount": 5
            }
        )

        print("prosody: " + prosody_container.id)
        # print(web_container.logs(follow=True))

if __name__ == "__main__":
    # docker_network_name = "meet.jitsi"
    stack_version = os.getenv("STACK_VERSION")
    http_port = os.getenv("HTTP_PORT")
    https_port = os.getenv("HTTPS_PORT")
    # config_dir = os.getenv("CONFIG")

    app = App()
    logging.info("Creating config dirs")
    app.create_config_tree()
    logging.info("Creating docker network")
    app.create_docker_network()
    logging.info("Starting jitsi services")





        # alpine = jitsi.alpine
        # container = client.containers.run(
        #     alpine.get("image"),
        #     name=alpine.get("container_name"),
        #     command="yes",
        #     # command="touch /alpine/file.log",
        #     environment=alpine.get("env"),
        #     ports=alpine.get("ports"),
        #     network=alpine.get("network"),
        #     volumes=alpine.get("volumes"),
        #     detach=True,
        #     remove=True
        # )
