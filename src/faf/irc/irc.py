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
        self.on('CLIENT_CONNECT', self.on_connect)
        self.on('CLIENT_DISCONNECT', self.on_disconnect)

    def on(self, msg, cb):
        return self.c.on(msg)(cb)

    def connect(self, username):
        self.my_username = username
        self.c.loop.create_task(self.c.connect())

    def disconnect(self):
        self.c.loop.create_task(self.c.disconnect())

    async def on_ping(self, message, **kwargs):
        self.c.send('PONG', message=message)

    async def _wait_on_motd(self):
        done, pending = await asyncio.wait(
            [self.c.wait("RPL_ENDOFMOTD"),
             self.c.wait("ERR_NOMOTD")],
            return_when=asyncio.FIRST_COMPLETED
        )
        for future in pending:
            future.cancel()

    async def on_connect(self, **kwargs):
        self.c.send('NICK', nick=self.username)
        self.c.send('USER', user=self.username, realname=self.username)
        await self._wait_on_motd()
        self.connected.emit()

    async def on_disconnect(self, **kwargs):
        self.diconnected.emit()
