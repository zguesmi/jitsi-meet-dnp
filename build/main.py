import logging
import os
import docker
import jitsi


def create_docker_network():
    try:
        client.networks.get(jitsi.docker_network_name)
    except docker.errors.NotFound as e:
        client.networks.create(jitsi.docker_network_name, driver="bridge")
    except:
        print('Error creating network: ' + jitsi.docker_network_name)
        exit()

if __name__ == "__main__":
    client = docker.from_env()
    create_docker_network()
    alpine = jitsi.alpine
    prosody = jitsi.prosody # should run first
    web = jitsi.web

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

    container = client.containers.run(
        web.get("image"),
        name=web.get("container_name"),
        # command="yes",
        environment=web.get("env"),
        ports=web.get("ports"),
        network=web.get("network"),
        volumes=web.get("volumes"),
        detach=True,
        # remove=True
    )

    print(container.id)
    print(container.logs())
