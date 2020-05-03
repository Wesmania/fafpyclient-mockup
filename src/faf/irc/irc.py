from dataclasses import dataclass
from enum import IntFlag, Enum, auto
from bottom.client import Client
from PySide2.QtCore import QObject, Signal
import asyncio

from faf.irc.ctcp import ctcp_dequote
from faf.irc.style import unstyle
from faf.tools.md5 import md5


class MessageType(Enum):
    MESSAGE = auto()
    NOTICE = auto()
    ACTION = auto()


class IrcMode(IntFlag):
    # These are specific to UnrealIRCd.
    OWNER = 16
    ADMIN = 8
    OP = 4
    HALFOP = 2
    VOICED = 1

    @classmethod
    def from_usermode(cls, prev, usermode_str):
        adding = True
        for char in usermode_str:
            if char == '+':
                adding = True
            elif char == '-':
                adding = False
            elif char in MODES:
                if adding:
                    prev |= MODES[char]
                else:
                    prev &= ~MODES[char]
        return prev


PREFICES = {
    '~': IrcMode.OWNER,
    '&': IrcMode.ADMIN,
    '@': IrcMode.OP,
    '%': IrcMode.HALFOP,
    '+': IrcMode.VOICED,
}


MODES = {
    'q': IrcMode.OWNER,
    'a': IrcMode.ADMIN,
    'o': IrcMode.OP,
    'h': IrcMode.HALFOP,
    'v': IrcMode.VOICED,
}


@dataclass
class IrcNickWithMode:
    nick: str
    mode: IrcMode

    @classmethod
    def from_nick_pfx(cls, pfx):
        return PREFICES.get(pfx, cls(0))

    @classmethod
    def from_nick(cls, nick):
        if not nick or nick[0] not in PREFICES:
            return cls(nick, IrcMode(0))
        mode = PREFICES(nick[0])
        return cls(nick[1:], mode)


class IrcClient(QObject):
    connected = Signal()
    disconnected = Signal()
    nickserv_identified = Signal()
    names = Signal(str, list)
    join = Signal(str, IrcNickWithMode)
    part = Signal(str, IrcNickWithMode, str)
    quit = Signal(IrcNickWithMode, str)
    topic = Signal(str, str)
    usermode = Signal(IrcNickWithMode, str)
    rename = Signal(IrcNickWithMode, IrcNickWithMode)
    message = Signal(IrcNickWithMode, str, str, MessageType)

    def __init__(self, host, port):
        QObject.__init__(self)
        self.my_username = None
        self.nickserv_password = None
        self._nickserv_identified = False
        self._nickserv_registered = False
        self.c = Client(host, port, ssl=False)
        self._on('CLIENT_CONNECT', self._on_connect)
        self._on('CLIENT_DISCONNECT', self._on_disconnect)
        self._on('PING', self._on_ping)
        self._on('RPL_NAMREPLY', self._on_names)
        self._on('JOIN', self._on_join)
        self._on('QUIT', self._on_quit)
        self._on('PART', self._on_part)
        self._on('RPL_TOPIC', self._on_topic)
        self._on('PRIVMSG', self._on_privmsg)
        self._on('NOTICE', self._on_notice)
        self._on('USERMODE', self._on_usermode)
        self._on('NICK', self._on_rename)

    def _on(self, msg, cb):
        return self.c.on(msg)(cb)

    def connect_(self, username, password):
        self.my_username = IrcNickWithMode(username, IrcMode(0))
        self.nickserv_password = md5(password)
        self.c.loop.create_task(self.c.connect())

    def disconnect_(self):
        self.c.loop.create_task(self.c.disconnect())

    async def _on_connect(self, **kwargs):
        self.c.send('NICK', nick=self.my_username.nick)
        self.c.send('USER', user=self.my_username.nick,
                    realname=self.my_username.nick)
        await self._wait_on_motd()
        self._nickserv_identify()
        self.connected.emit()

    async def _wait_on_motd(self):
        done, pending = await asyncio.wait(
            [self.c.wait("RPL_ENDOFMOTD"),
             self.c.wait("ERR_NOMOTD")],
            return_when=asyncio.FIRST_COMPLETED
        )
        for future in pending:
            future.cancel()

    async def _on_disconnect(self, **kwargs):
        self._nickserv_identified = False
        self.diconnected.emit()

    async def _on_ping(self, message, **kwargs):
        self.c.send('PONG', message=message)

    def _on_names(self, channel_name, users, **kwargs):
        users = [IrcNickWithMode.from_nick(u) for u in users]
        self.names.emit(channel_name, users)

    def _on_join(self, channel_name, nick=None, **kwargs):
        if nick is None:
            return
        nick = IrcNickWithMode.from_nick(nick)
        self.join.emit(channel_name, nick)

    def _on_part(self, channel_name, message, nick=None, **kwargs):
        if nick is None:
            return
        nick = IrcNickWithMode.from_nick(nick)
        self.part.emit(channel_name, nick, message)

    def _on_quit(self, message, nick=None, **kwargs):
        if nick is None:
            return
        nick = IrcNickWithMode.from_nick(nick)
        self.part.emit(nick, message)

    def _on_topic(self, channel, message, **kwargs):
        self.topic.emit(channel, message)

    def _on_usermode(self, modes, nick=None, **kwargs):
        if nick is None:
            return
        nick = IrcNickWithMode.from_nick(nick)
        self.usermode.emit(nick, modes)

    def _on_rename(self, new_nick, nick=None, **kwargs):
        if nick is None:
            return
        nick = IrcNickWithMode.from_nick(nick)
        new_nick = IrcNickWithMode.from_nick(nick)
        self.rename.emit(nick, new_nick)

    def _on_message(self, target, message, default_type, nick=None):
        if nick is None:
            return
        nick = IrcNickWithMode.from_nick(nick)
        if nick.nick.lower() == 'nickserv':
            return self._handle_nickserv(message)

        messages = ctcp_dequote(message)
        for msg in messages:
            if isinstance(msg, tuple):
                self._on_action(nick, target, msg)
            else:
                self._on_msg(nick, target, msg, default_type)

    def _on_privmsg(self, target, message, nick=None, **kwargs):
        self._on_message(target, message, MessageType.MESSAGE, nick)

    def _on_notice(self, target, message, nick=None, **kwargs):
        self._on_message(target, message, MessageType.NOTICE, nick)

    def _on_action(self, nick, target, message):
        if message[0] != 'ACTION':
            return
        if len(message) < 2:
            return
        message = unstyle(message[1])
        self._on_msg(nick, target, message, MessageType.ACTION)

    def _on_msg(self, nick, target, message, type_):
        message = unstyle(message)
        self.message.emit(nick, target, message, type_)

    # TODO - below bit might be incomplete. Things might break if we changed
    # our username or if there's a user with the same username on IRC because
    # of a stale session. Identify and fix.
    def _handle_nickserv(self, message):
        ident_strings = ["registered under your account", "Password accepted",
                         "You are already identified."]
        if any(s in message for s in ident_strings):
            if not self._nickserv_identified:
                self._nickserv_identified = True
                self.nickserv_identified.emit()
        elif "isn't registered" in message:
            self._nickserv_register()
        elif f"Nickname {self.my_username.nick} registered." in message:
            self._nickserv_identify()

    def _nickserv_identify(self):
        if self._nickserv_identified:
            return
        self._send_to_nickserv(f'identify {self.my_username.nick} '
                               f'{self.nickserv_password}')

    def _nickserv_register(self):
        if self._nickserv_registered:
            return
        self._send_to_nickserv(f'register {self.nickserv_password} '
                               f'{self.my_username.nick}@users.faforever.com')
        self._nickserv_registered = True

    def _send_to_nickserv(self, msg):
        self.c.send('PRIVMSG', target="NickServ", message=msg)
