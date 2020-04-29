from bottom.client import Client
import asyncio
import sys


class Irc:
    def __init__(self, host, port, username):
        self.username = username
        self.c = Client(host, port, ssl=False)

        self.c.on('CLIENT_CONNECT')(self.on_connect)
        self.c.on('CLIENT_DISCONNECT')(self.on_disconnect)
        self.c.on('PING')(self.on_ping)
        self.c.on('RPL_NAMREPLY')(self.on_names)
        self.c.on('JOIN')(self.on_join)
        self.c.on('QUIT')(self.on_quit)
        self.c.on('PART')(self.on_part)
        self.c.on('RPL_TOPIC')(self.on_topic)
        self.c.on('MESSAGE')(self.on_message)
        self.c.on('PRIVMSG')(self.on_privmsg)
        self.c.on('ACTION')(self.on_action)
        self.c.on('USERMODE')(self.on_usermode)
        self.c.raw_handlers.append(self.on_raw)

    def on(self, msg, cb):
        return self.c.on(msg)(cb)

    async def connect(self):
        await self.c.connect()

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
        self.c.send('JOIN', channel="#aeolus")

    async def on_disconnect(self, **kwargs):
        # TODO
        print("Disconnect")

    async def on_names(self, **kwargs):
        # TODO
        pass
        # print(f"Names: {kwargs}")

    async def on_raw(self, nxt, msg):
        print(msg, file=sys.stderr)
        await nxt(msg)

    async def on_join(self, **kwargs):
        # TODO
        print(f"Join: {kwargs}")

    async def on_part(self, **kwargs):
        # TODO
        print(f"Part: {kwargs}")

    async def on_quit(self, **kwargs):
        # TODO
        print(f"Quit: {kwargs}")

    async def on_notice(self, **kwargs):
        # TODO
        print(f"Notice: {kwargs}")

    async def on_message(self, **kwargs):
        # TODO
        print(f"Message: {kwargs}")

    async def on_privmsg(self, **kwargs):
        # TODO
        print(f"Privmsg: {kwargs}")

    async def on_action(self, **kwargs):
        # TODO
        print(f"Action: {kwargs}")

    async def on_usermode(self, **kwargs):
        # TODO
        print(f"Usermode: {kwargs}")

    async def on_topic(self, **kwargs):
        # TODO
        print(f"Topic: {kwargs}")


if __name__ == "__main__":
    irc = Irc('irc.faforever.com', 6667, "foobar_")
    loop = asyncio.get_event_loop()
    t = loop.create_task(irc.connect())
    loop.run_forever()
