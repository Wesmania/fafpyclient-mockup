from faf.models.base import ModelItem
from faf.irc.irc import IrcMode


class Chatter(ModelItem):
    def __init__(self, nick_with_mode):
        ModelItem.__init__(self)
        self.nick = nick_with_mode.nick
        self._add_obs('mode', nick_with_mode.mode)
        self._add_obs('player', None)

    @property
    def id_key(self):
        return self.nick

    @property
    def is_op(self):
        return self.mode >= IrcMode.OP
