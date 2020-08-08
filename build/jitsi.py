import logging
import os
import docker
import shutil
import signal

import config


# logging
log = config.log

# one docker client instance
docker_client = docker.from_env()


class DockerHelper:

    @staticmethod
    def remove_container_if_present(container_name):
        try:
            container = docker_client.containers.get(container_name)
            log.info(f"Removing existing container [name:{container_name}]")
            container.remove(v=True, force=True)
        except:
            pass

    @staticmethod
    def create_container(image, container_name, ports, volumes, env, restart_policy):
        try:
            container = docker_client.containers.create(
                image,
                name=container_name,
                environment=env,
                ports=ports,
                volumes=volumes,
                restart_policy=restart_policy,
            )
            log.debug(f"Created container [name:{container.name}, id:{container.id}]")
            return container
        except Exception as e:
            log.error(f"Error creating container [name:{container_name}]")
            log.error(e)
            return None

    @staticmethod
    def create_network(network_name):
        try:
            existing_network = docker_client.networks.get(network_name)
            log.debug(f"Docker network already exists [name:{existing_network.name}]")
            return existing_network
        except docker.errors.NotFound as e:
            log.info(f"Creating docker network [name:{network_name}]")
            return docker_client.networks.create(network_name, driver="bridge")
        except Exception as e:
            log.error(f"Error creating docker network [name:{network_name}]")
            log.error(e)
            return None


class Service:

    def __init__(self, service_config, network):
        DockerHelper.remove_container_if_present(service_config["container_name"])
        self.container = DockerHelper.create_container(
            image=service_config["image"],
            container_name=service_config["container_name"],
            ports=service_config["ports"],
            volumes=service_config["volumes"],
            env=service_config["env"],
            restart_policy=service_config["restart_policy"]
        )
        if network is not None:
            network.connect(container=self.container, aliases=service_config["network_aliases"])
            log.debug(f"Connected container to network [container:{self.container.name}, network:{network.name}]")

    def get_name(self):
        return self.container.name

    def start(self):
        try:
            log.debug(f"Starting container [name:{self.container.name}, id:{self.container.id}]")
            self.container.start()
            log.debug(f"Started container [name:{self.container.name}, id:{self.container.id}]")
        except Exception as e:
            log.error(f"Error starting container [name:{self.container.name}]")
            log.error(e)
    
    def remove(self):
        self.container.remove(v=True, force=True)


class App():

    def __init__(self):
        self.docker_network = DockerHelper.create_network(config.docker_network_name)
        if self.docker_network is None:
            exit(1)
        if os.path.exists(config.config_root_dir):
            log.info(f"Cleaning possible old config files [root_dir:{config.config_root_dir}]")
            for folder in os.listdir(config.config_root_dir):
                shutil.rmtree(os.path.join(config.config_root_dir, folder))
        signal.signal(signal.SIGINT, self.tear_down)
        signal.signal(signal.SIGTERM, self.tear_down)

    def run(self):
        log.info("Running XMPP server (Prosody)")
        self.xmpp_service = Service(service_config=config.xmpp, network=self.docker_network)
        self.xmpp_service.start()
        log.info("Running focus component (Jicofo)")
        self.jicofo_service = Service(service_config=config.jicofo, network=self.docker_network)
        self.jicofo_service.start()
        log.info("Running video bridge (Jvb)")
        self.jvb_service = Service(service_config=config.jvb, network=self.docker_network)
        self.jvb_service.start()
        log.info("Running web component")
        self.web_component = Service(service_config=config.web, network=self.docker_network)
        self.web_component.start()
        log.info("All services are up")
        self.xmpp_service.container.wait()

    def tear_down(self):
        self.web_component.remove()
        self.jvb_service.remove()
        self.jicofo_service.remove()
        self.xmpp_service.remove()


if __name__ == "__main__":
    app = App()
    try:
        app.run()
    except Exception as e:
        app.tear_down()
        log.exception(e)
        exit(1)
