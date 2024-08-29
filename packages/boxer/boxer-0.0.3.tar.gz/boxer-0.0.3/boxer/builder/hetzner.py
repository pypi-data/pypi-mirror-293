# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""Build images on Hetzner

Uses Hetzner API to create a instance and then to create a snapshot
"""

import asyncio
import contextlib
import logging
import os
import warnings

try:
    import hcloud
    from hcloud.servers import ServerCreatePublicNetwork
except ImportError:
    hcloud = None
    logging.getLogger(__name__).warning("Hetzner providednot available due to missing hcloud library")

from boxer import Builder, __version__
from boxer.common import exceptions
from boxer.transport import SSH

LOGGER = logging.getLogger(__name__)


class Hetzner(Builder):
    """Build images on Hetzner

    Attributes:
        token: Hetzner authentication token. Value is taken from HCLOUD_TOKEN environment variable if not set
        name: Name of the image to be build. If not set, build_name is used
        labels: Labels to apply to the image
        protect: If true, enable protection of the image
        image: Base image to build from
        architecture: Architecture of the image
        server_type: Server type to be used during the build
        location: Location used during the build
        port: Transport port
        username: Transport username
        password: Transport password
    """
    token = os.environ.get("HCLOUD_TOKEN", None)
    name = None
    labels = None
    protect = False
    image = None
    architecture = "x86"
    server_type = None
    location = None
    port = None
    username = None
    password = None
    _boxer_ssh_key = None
    _boxer_server = None

    def __init__(self, *a, **kw):
        if hcloud is None:
            raise exceptions.MissingRequirement("hcloud is required to use Hetzner builder")
        warnings.warn("Hetzner client isn't async ready yet. This will impact parallel execution")
        if self.name is None:
            self.name == self.build_name  # pylint: disable=pointless-statement
        super().__init__(*a, **kw)

    @contextlib.contextmanager
    def client(self):
        """Context manager to open an Hetzner client"""
        client = hcloud.Client(self.token, application_name="Boxer", application_version=__version__)
        yield client

    async def prepare(self):
        await super().prepare()
        with self.client() as client:
            if isinstance(self.image, int):
                image = client.images.get_by_id(self.image)
            else:
                image = client.images.get_by_name(name=self.image, architecture=self.architecture)

            if image is None:
                raise exceptions.BoxerException(f"Unable to locate image {self.image}")
            server_args = {
                "image": image,
                "name": f"boxer-{self.uuid}",
                "public_net": ServerCreatePublicNetwork(),
                "server_type": client.server_types.get_by_name(self.server_type),
                "location": client.locations.get_by_name(self.location)
            }
            LOGGER.info("Using image %s", image.id)

            if isinstance(self.transport, SSH):
                self._boxer_ssh_key = client.ssh_keys.create(name=f"boxer-{self.uuid}", public_key=self.transport.client_key.export_public_key().decode("ascii").splitlines()[0])
                server_args["ssh_keys"] = [self._boxer_ssh_key]

            self._boxer_server = client.servers.create(**server_args)
            if self._boxer_server.root_password:
                self.password = self._boxer_server.root_password
                self.transport.password = self.password

            LOGGER.info("Waiting for server creation")
            self._boxer_server.action.wait_until_finished()
            self.transport.port = self.port
            self.transport.address = self._boxer_server.server.public_net.ipv4.ip

    async def finish(self):
        await super().finish()
        with self.client() as client:
            self._boxer_server.server.client = client
            self._boxer_server.server.reload()
            while self._boxer_server.server.status in (self._boxer_server.server.STATUS_RUNNING, self._boxer_server.server.STATUS_STOPPING):
                LOGGER.info("Waiting for server to stop")
                await asyncio.sleep(10)
                self._boxer_server.server.reload()
            if self._boxer_server.server.status != self._boxer_server.server.STATUS_OFF:
                raise exceptions.BoxerException(f"Inconsistent server status: {self._boxer_server.status}")

            image = self._boxer_server.server.create_image(self.name, "snapshot", self.labels)
            LOGGER.info("Creating image")
            image.action.wait_until_finished()
            if self.protect:
                action = image.image.change_protection(True)
                LOGGER.info("Protecting image")
                action.wait_until_finished()

    async def cleanup(self):
        await super().cleanup()
        if self._boxer_server is not None:
            with self.client() as client:
                self._boxer_server.server.client = client
                self._boxer_server.server.reload()
                if self._boxer_server.server.status in (self._boxer_server.server.STATUS_RUNNING, self._boxer_server.server.STATUS_STARTING, self._boxer_server.server.STATUS_STOPPING):
                    action = self._boxer_server.server.power_off()
                    LOGGER.info("Forcing poweroff of server")
                    action.wait_until_finished()
                action = self._boxer_server.server.delete()
                LOGGER.info("Deleting server")
                action.wait_until_finished()
                if self._boxer_ssh_key:
                    self._boxer_ssh_key.client = client
                    LOGGER.info("Deleting temporary SSH key")
                    self._boxer_ssh_key.delete()
