import asyncio
import logging
import os
from time import sleep

import rich
import sqlalchemy
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrNoServers
from sqlalchemy.exc import IntegrityError

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.consensus.local_config import NATS_HOST, NATS_PORT
from decentnet.modules.comm.relay import Relay
from decentnet.modules.db.base import session_scope
from decentnet.modules.db.models import AliveBeam
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


class Consumer:
    def __init__(self, relay: Relay):
        self.nats_client = NATS()
        self.relay = relay
        while not self.relay.beam_pub_key:
            sleep(1)

        self.id = self.relay.beam_pub_key
        try:
            asyncio.run(self.nats_client.connect(servers=[f"nats://{NATS_HOST}:{NATS_PORT}"]))
        except ErrNoServers:
            rich.print("[red]Unable to connect to NATS server, relaying unavailable[/red]")
        self.channel_name = self.id
        asyncio.run(self.save_to_db(False))

        while not relay.beam.connected:
            logger.debug(f"Consumer waiting for beam {self.id} to connect")
            sleep(0.5)
        asyncio.run(self.mark_ready(True))
        asyncio.run(self.start())

    async def save_to_db(self, ready: bool):
        async with session_scope() as session:
            try:
                csd = AliveBeam(pub_key=self.id, ready=ready)
                session.add(csd)
                await session.commit()
                logger.debug(f"Saved alive beam {csd.pub_key}")
            except (IntegrityError, sqlalchemy.exc.IntegrityError):
                await session.rollback()

    async def mark_ready(self, ready: bool):
        await AliveBeam.mark_beam_ready(self.channel_name, ready)

    async def start(self):
        await self.subscribe_to_channel()

    async def subscribe_to_channel(self):
        await self.nats_client.subscribe(self.channel_name, cb=self.process_message)
        logger.info(f"Consumer subscribed on channel {self.channel_name} PID: {os.getpid()}")

    async def process_message(self, msg):
        message_data = msg.data
        logger.debug(
            f"Consumer {self.channel_name} sending message to {self.relay.beam.client.host}:{self.relay.beam.client.port}")
        self.relay.beam.client.send_message(message_data, ack=False)
