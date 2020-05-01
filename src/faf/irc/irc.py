from bottom.client import Client
from PySide2.QtCore import QObject, Signal
import asyncio


class Irc(QObject):
    connected = Signal()
    disconnected = Signal()

    def __init__(self, host, port):
        QObject.__init__(self)
        self.my_username = None
        self.c = Client(host, port, ssl=False)
        self.on('CLIENT_CONNECT', self._on_connect)
        self.on('CLIENT_DISCONNECT', self._on_disconnect)
        self.on('PING', self._on_ping)

    def on(self, msg, cb):
        return self.c.on(msg)(cb)

    def connect_(self, username):
        self.my_username = username
        self.c.loop.create_task(self.c.connect())

    def disconnect_(self):
        self.c.loop.create_task(self.c.disconnect())

    async def _on_ping(self, message, **kwargs):
        self.c.send('PONG', message=message)

    async def _wait_on_motd(self):
        done, pending = await asyncio.wait(
            [self.c.wait("RPL_ENDOFMOTD"),
             self.c.wait("ERR_NOMOTD")],
            return_when=asyncio.FIRST_COMPLETED
        )
        for future in pending:
            future.cancel()

    async def _on_connect(self, **kwargs):
        self.c.send('NICK', nick=self.my_username)
        self.c.send('USER', user=self.my_username, realname=self.my_username)
        await self._wait_on_motd()
        self.connected.emit()

    async def _on_disconnect(self, **kwargs):
        self.diconnected.emit()
