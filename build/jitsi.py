import logging
import os
import docker
import shutil
import signal
import threading
import time

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
                # detach=True,
                # restart_policy=restart_policy,
                # remove=True
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

    def __init__(self, config, network):
        DockerHelper.remove_container_if_present(config.container_name)
        self.container = DockerHelper.create_container(
            image=config.image,
            container_name=config.container_name,
            ports=config.ports,
            volumes=config.volumes,
            env=config.env,
            network=self.docker_network,
            network_aliases=config.network_aliases,
            restart_policy=config.restart_policy
        )
        if network is not None:
            network.connect(container=self.container, aliases=config.network_aliases)
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
        self.container.stop()
        self.container.remove(v=True, force=True)


class JitsiApp():

    def __init__(self):
        self.docker_network = DockerHelper.create_network(config.docker_network_name)
        if self.docker_network is None:
            exit(1)
        if os.path.exists(config.config_root_dir):
            log.info("Cleaning possible old config files [root_dir:{}]".format(config.config_root_dir))
            for folder in os.listdir(config.config_root_dir):
                shutil.rmtree(os.path.join(config.config_root_dir, folder))
        signal.signal(signal.SIGINT, self.tear_down)
        signal.signal(signal.SIGTERM, self.tear_down)

    # def setup(self):
    #     self.docker_network = DockerHelper.create_network(self.docker_network_name)
    #     if self.docker_network is None:
    #         exit(1)
    #     self.__clean_config_tree()

    # def __clean_config_tree(self):
    #     if os.path.exists(self.config_root_dir):
    #         log.info("Cleaning possible old config files [root_dir:{}]".format(self.config_root_dir))
    #         for folder in os.listdir(self.config_root_dir):
    #             shutil.rmtree(os.path.join(self.config_root_dir, folder))

    def up(self):
        log.info("Running XMPP server (Prosody)")
        self.xmpp_service = Service(config=config.xmpp, network=self.docker_network)
        self.xmpp_service.start()

        log.info("Running focus component (Jicofo)")
        self.jicofo_service = Service(config=config.jicofo, network=self.docker_network)
        self.jicofo_service.start()

        log.info("Running video bridge (Jvb)")
        self.jvb_service = Service(config=config.jvb, network=self.docker_network)
        self.jvb_service.start()

        log.info("Running web component")
        self.web_component = Service(config=config.web, network=self.docker_network)
        self.web_component.start()

        log.info("All services are up")
        self.xmpp_service.container.wait()

    def tear_down(self):
        self.web_component.remove()
        self.jvb_service.remove()
        self.jicofo_service.remove()
        self.xmpp_service.remove()

    # """
    # Jitsi XMPP component (prosody).
    # """
    # def start_xmpp_server(self):
    #     xmpp_service = Service(config=config.xmpp, network=self.docker_network)
    #     xmpp_service.start()
    #     return xmpp_service

    # """
    # Jitsi web component.
    # """
    # def start_web_component(self):
    #     web_component = Service(config=config.web, network=self.docker_network)
    #     web_component.start()
    #     return web_component

    # """
    # Jitsi focus component.
    # """
    # def start_focus_component(self):
    #     jicofo_service = Service(config=config.jicofo, network=self.docker_network)
    #     jicofo_service.start()
    #     return jicofo_service

    # """
    # Jitsi video bridge component.
    # """
    # def start_video_bridge(self):
    #     self.jvb_service = Service(config=config.jvb, network=self.docker_network)
    #     self.jvb_service.start()


if __name__ == "__main__":
    jitsi = JitsiApp()
    jitsi.setup()
    try:
        jitsi.up()
    except Exception as e:
        jitsi.tear_down()
        log.error("Error in main thread")
        log.exception(e)
        exit(1)
