import logging
import re
import docker
from time import sleep

LOCALSTACK_NAME = "localstack/localstack"
LOCALSTACK_TAG = "latest"

MAX_PORT_CONNECTION_ATTEMPTS = 10
MAX_LOG_COLLECTION_ATTEMPTS = 120
POLL_INTERVAL = 1
NUM_LOG_LINES = 10

ENV_DEBUG = "DEBUG"
ENV_USE_SSL = "USE_SSL"
ENV_DEBUG_DEFAULT = "1"
LOCALSTACK_EXTERNAL_HOSTNAME = "HOSTNAME_EXTERNAL"
DEFAULT_CONTAINER_ID = "localstack-main"

DOCKER_CLIENT = docker.from_env()


class Container:
    @staticmethod
    def create_localstack_container(
        pull_new_image,
        image_name,
        image_tag,
        gateway_listen,
        environment_variables,
    ):
        environment_variables = environment_variables or {}
        environment_variables["GATEWAY_LISTEN"] = gateway_listen

        image_name_or_default = LOCALSTACK_NAME if image_name is None else image_name
        image_exists = (
            True
            if len(DOCKER_CLIENT.images.list(name=image_name_or_default))
            else False
        )

        port = gateway_listen.split(":")[1]
        full_port_edge = {port: port}

        if pull_new_image or not image_exists:
            logging.info("Pulling latest image")
            DOCKER_CLIENT.images.pull(image_name_or_default, image_tag)

        return DOCKER_CLIENT.containers.run(
            image_name_or_default,
            ports=full_port_edge,
            environment=environment_variables,
            detach=True,
        )

    @staticmethod
    def wait_for_ready(container, pattern):
        attempts = 0

        while True:
            logs = container.logs(tail=NUM_LOG_LINES).decode("utf-8")
            if re.search(pattern, logs):
                return

            sleep(POLL_INTERVAL)
            attempts += 1

            if attempts >= MAX_LOG_COLLECTION_ATTEMPTS:
                raise "Could not find token: " + pattern.toString() + "in logs"
