import logging
import os
import docker
import secrets
import string
import services


version = "stable-4548"
CONFIG = os.getenv("CONFIG")
HTTP_PORT = os.getenv("HTTP_PORT")
HTTPS_PORT = os.getenv("HTTPS_PORT")
DOCKER_NETWORK = "meet.jitsi"

def generate_random_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(16))

if __name__ == "__main__":
    client = docker.from_env()
    client.networks.create(services.docker_network_name)

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
