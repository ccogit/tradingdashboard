import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class IBGatewayClient:
    def __init__(self):
        self.ib = None
        self.host = ""
        self.port = 0
        self.client_id = 0
        self.is_connected = False
        self.last_error: Optional[str] = None
        self._reconnect_task: Optional[asyncio.Task] = None

    async def connect(self, host: str, port: int, client_id: int) -> None:
        self.host = host
        self.port = port
        self.client_id = client_id
        await self._do_connect()

    async def _do_connect(self) -> None:
        try:
            from ib_async import IB
            self.ib = IB()
            await self.ib.connectAsync(self.host, self.port, clientId=self.client_id)
            self.is_connected = True
            self.last_error = None
            self.ib.disconnectedEvent += self._on_disconnected
            logger.info(f"Connected to IB Gateway at {self.host}:{self.port}")
        except Exception as e:
            self.is_connected = False
            self.last_error = str(e)
            logger.warning(f"IB Gateway connection failed: {e}")
            self._schedule_reconnect()

    def _on_disconnected(self) -> None:
        self.is_connected = False
        logger.warning("Disconnected from IB Gateway")
        self._schedule_reconnect()

    def _schedule_reconnect(self, delay: int = 5) -> None:
        if self._reconnect_task is None or self._reconnect_task.done():
            self._reconnect_task = asyncio.create_task(self._reconnect_loop(delay))

    async def _reconnect_loop(self, initial_delay: int) -> None:
        delay = initial_delay
        while not self.is_connected:
            await asyncio.sleep(delay)
            logger.info(f"Attempting IB Gateway reconnect...")
            await self._do_connect()
            delay = min(delay * 2, 60)

    async def disconnect(self) -> None:
        if self.ib and self.is_connected:
            self.ib.disconnect()
        self.is_connected = False


ib_client = IBGatewayClient()
