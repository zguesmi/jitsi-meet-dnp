import logging
import os
import docker
import services


if __name__ == "__main__":
    client = docker.from_env()

    # create docker network
    client.networks.create(services.docker_network_name, driver="bridge")

    alpine = services.alpine

    container = client.containers.run(
        alpine.get("image"),
        name=alpine.get("container_name"),
        command="touch /alpine/file.log",
        # command="cat /etc/hosts >> /alpine/file.log && tail -f /alpine/file.log",
        environment=alpine.get("env"),
        ports=alpine.get("ports"),
        network=alpine.get("network"),
        volumes=alpine.get("volumes"),
        detach=True,
        remove=True
    )

    print(container.id)
    print(container.logs())
    print(generate_random_password())
