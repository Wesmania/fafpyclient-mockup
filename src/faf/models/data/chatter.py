from enum import IntFlag
from faf.models.base import ModelItem


class IRCMode(IntFlag):
    # These are specific to UnrealIRCd.
    OWNER = 1
    ADMIN = 2
    OP = 4
    HALFOP = 8
    VOICED = 16

    @classmethod
    def from_nick_pfx(cls, pfx):
        return PREFICES.get(pfx, cls(0))

    @classmethod
    def from_nick(cls, nick):
        if not nick:
            return cls(0)
        return cls.from_nick_pfx(nick[0])

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

    @classmethod
    def strip(cls, nick):
        if nick and nick[0] in PREFICES:
            return nick[1:]
        else:
            return nick


PREFICES = {
    '~': IRCMode.OWNER,
    '&': IRCMode.ADMIN,
    '@': IRCMode.OP,
    '%': IRCMode.HALFOP,
    '+': IRCMode.VOICED,
}


MODES = {
    'q': IRCMode.OWNER,
    'a': IRCMode.ADMIN,
    'o': IRCMode.OP,
    'h': IRCMode.HALFOP,
    'v': IRCMode.VOICED,
}


class Chatter(ModelItem):
    def __init__(self, nick):
        ModelItem.__init__(self)
        self.nick = nick    # When renaming, just remove and add.
        self._add_obs('mode', IRCMode(0))
        self._add_obs('player', None)

    @classmethod
    def from_nick(cls, nick):
        mode = IRCMode.from_nick(nick)
        c = cls(IRCMode.strip(nick))
        c.mode = mode
        return c

    @property
    def id_key(self):
        return self.nick
