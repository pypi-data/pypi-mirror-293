import asyncio
import logging

from nats.aio.client import Client
from nats.aio.errors import ErrNoServers

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


class BlockPublisher:
    _instance = None  # Class variable to hold the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BlockPublisher, cls).__new__(cls)
            # Initialize the instance once
            cls._instance.__init_once__(*args, **kwargs)
        return cls._instance

    def __init_once__(self, host="127.0.0.1", port=4222):
        """
        Initializes the NatsPublisher with connection to the NATS server, ensuring
        that this initialization only happens once.
        """
        try:
            # Create a NATS client instance
            self.nats_client = nc = Client()

            # Attempt to connect to the NATS server
            asyncio.run(nc.connect(servers=[f"nats://{host}:{port}"]))

            connection_info = f"NATS Connection Info:\nHost: {host}\nPort: {port}"
            logger.debug(connection_info)

        except ErrNoServers as e:
            logger.error(f'NATS client unable to connect, not able to relay beams. Error: {e}')

    def publish_message(self, channel: str, message: bytes):
        """
        Publishes a message to a given channel.
        """
        self.nats_client.publish(channel, message)
