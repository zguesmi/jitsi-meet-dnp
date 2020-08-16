import docker
import logging
import os
from pyfiglet import Figlet
import shutil
import signal

import utils
from utils import DockerHelper
from utils import AppConfig

# logging
log = utils.get_logger()


class Service:
    """
    A docker service that runs a Jitsi component.
    """

    def __init__(self, config, network):
        DockerHelper.remove_container_if_present(config.container_name)
        self.container = DockerHelper.create_container(config)
        if self.container is None:
            utils.exit_app()
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
        try:
            self.container.remove(v=True, force=True)
            log.info(f"Removed container [name:{self.container.name}]")
        except Exception as e:
            log.error(f"Error removing container [name:{self.container.name}]")


class App():

    def __init__(self, app_config):
        self.app_config = app_config
        signal.signal(signal.SIGINT, self.tear_down)
        signal.signal(signal.SIGTERM, self.tear_down)

    def print_versions(self):
        print(Figlet().renderText("Jitsi Meet"))
        print(f" > Jitsi version: {self.app_config.stack_version}")
        print(f" > Docker version: {DockerHelper.get_version()}")
        print()

    def setup(self):
        self.purge_config_files()
        self.docker_network = DockerHelper.create_network(self.app_config.docker_network_name)
        if self.docker_network is None:
            utils.exit_app()
        xmpp_image = DockerHelper.pull_image(self.app_config.xmpp_container_config.image)
        web_image = DockerHelper.pull_image(self.app_config.web_container_config.image)
        jicofo_image = DockerHelper.pull_image(self.app_config.jicofo_container_config.image)
        jvb_image = DockerHelper.pull_image(self.app_config.jvb_container_config.image)
        if None in [xmpp_image, web_image, jicofo_image, jvb_image]:
            utils.exit_app()

    def purge_config_files(self):
        log.info(f"Purging existing config files [root_dir:{self.app_config.config_root_dir}]")
        path = self.app_config.config_root_dir
        if os.path.exists(path):
            for folder in os.listdir(path):
                shutil.rmtree(os.path.join(path, folder))

    def run(self):
        # create all containers before starting any one of them
        self.xmpp_service = Service(config=self.app_config.xmpp_container_config, network=self.docker_network)
        self.jicofo_service = Service(config=self.app_config.jicofo_container_config, network=self.docker_network)
        self.jvb_service = Service(config=self.app_config.jvb_container_config, network=self.docker_network)
        self.web_component = Service(config=self.app_config.web_container_config, network=self.docker_network)
        log.info("Running XMPP server (Prosody)")
        self.xmpp_service.start()
        log.info("Running focus component (Jicofo)")
        self.jicofo_service.start()
        log.info("Running video bridge (Jvb)")
        self.jvb_service.start()
        log.info("Running web component")
        self.web_component.start()
        log.info("All services are up")
        try:
            self.xmpp_service.container.wait(condition="removed")
        except Exception as e:
            log.error("Cannot wait XMPP service anymore")
            self.tear_down()

    def print_secrets(self):
        flag_length = 58
        log.info("#" * flag_length)
        log.info(f"jicofo_component_secret: {self.app_config.secrets.jicofo_component_secret}")
        log.info(f"jicofo_auth_password: {self.app_config.secrets.jicofo_auth_password}")
        log.info(f"jvb_auth_password: {self.app_config.secrets.jvb_auth_password}")
        log.info(f"jigasi_xmpp_password: {self.app_config.secrets.jigasi_xmpp_password}")
        log.info(f"jibri_recorded_password: {self.app_config.secrets.jibri_recorded_password}")
        log.info(f"jibri_xmpp_password: {self.app_config.secrets.jibri_xmpp_password}")
        log.info("#" * flag_length)

    def tear_down(self):
        self.web_component.remove()
        self.jvb_service.remove()
        self.jicofo_service.remove()
        self.xmpp_service.remove()
        self.purge_config_files()


if __name__ == "__main__":
    app_config = AppConfig()
    app = App(app_config)
    try:
        app.print_versions()
        app.setup()
        app.run()
        app.print_secrets()
    except Exception as e:
        app.tear_down()
        log.exception(e)
        utils.exit_app()
