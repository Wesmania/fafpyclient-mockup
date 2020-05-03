from typing import List

from faf.models.data.channel import Channel, ChannelID
from faf.models.data.chatter import Chatter
from faf.models.data.chatline import ChatLine
from faf.irc.irc import IrcNickWithMode, IrcMode, MessageType


# TODO - move some bits that have to do with irc format to irc module.
class ModelChatUpdater:
    def __init__(self, models, irc):
        self._models = models
        self._irc = irc
        self._chat_filter = lambda _: False

        self._irc.disconnected.connect(self.on_disconnect)
        self._irc.names.connect(self.on_names)
        self._irc.join.connect(self.on_join)
        self._irc.part.connect(self.on_part)
        self._irc.quit.connect(self.on_quit)
        self._irc.topic.connect(self.on_topic)
        self._irc.message.connect(self.on_message)
        self._irc.usermode.connect(self.on_usermode)
        self._irc.rename.connect(self.on_rename)

    @property
    def _players(self):
        return self._models.players

    @property
    def _chat(self):
        return self._models.chat

    def _add_or_update_from_nick(self, channel, nick: IrcNickWithMode):
        if nick.nick not in channel.chatters:
            new = Chatter(nick)
            if new.nick in self._players:
                new.player = self._players[new.nick]
            channel.chatters.add(new)
            channel.chatters.added.on_next(new)
        else:
            existing = channel.chatters[nick.nick]
            existing.mode = nick.mode

    def _remove_from_nick(self, channel, nick: IrcNickWithMode):
        if nick.nick not in channel.chatters:
            return
        to_remove = channel.chatters[nick.nick]
        channel.chatters.remove(to_remove)
        channel.chatters.removed.on_next(to_remove)

    def _remove_from_all(self, nick: IrcNickWithMode):
        for channel in self._chat.values():
            self._remove_from_nick(channel, nick)

    def _update_mode(self, channel, nick: IrcNickWithMode, modes):
        if nick.nick not in channel.chatters:
            return
        chatter = channel.chatters[nick.nick]
        new_mode = IrcMode.from_usermode(chatter.mode, modes)
        chatter.mode = new_mode

    def _add_channel(self, id_: ChannelID):
        if id_ in self._chat:
            return
        ch = Channel(id_)
        self._chat.add(ch)
        self._chat.added.on_next(ch)

    def _remove_channel(self, id_: ChannelID):
        if id_ not in self._chat:
            return
        ch = self._chat[id_]
        self._chat.remove(ch)
        self._chat.removed.on_next(ch)

    def on_disconnect(self):
        # FIXME - for persisting channel contents we'll want to emit a list of
        # removed channels here
        self._chat.clear()
        self._chat.cleared.on_next(None)

    def on_names(self, channel_name, users: List[IrcNickWithMode]):
        channel_id = ChannelID.public(channel_name)
        if channel_id not in self._chat:
            return
        channel = self._chat[channel_id]
        for nick in users:
            self._add_or_update_from_nick(channel, nick)

    def on_join(self, channel_name, nick: IrcNickWithMode):
        channel_id = ChannelID.public(channel_name)
        if nick.nick == self._irc.my_username:
            self._add_channel(channel_id)
        if channel_id not in self._chat:
            return
        channel = self._chat[channel_id]
        self._add_or_update_from_nick(channel, nick)

    def on_part(self, channel_name, nick: IrcNickWithMode, message):
        channel_id = ChannelID.public(channel_name)
        if channel_id not in self._chat:
            return
        channel = self._chat[channel_id]
        self._remove_from_nick(channel, nick)

        if nick == self._irc.my_username:
            self._remove_channel(channel_id)

    def on_quit(self, nick: IrcNickWithMode, message):
        self._remove_from_all(nick)

    def on_usermode(self, nick: IrcNickWithMode, modes):
        for channel in self._chat.values():
            self._update_mode(channel, nick, modes)

    def on_topic(self, channel, message):
        channel_id = ChannelID.public(channel)
        if channel_id not in self._chat:
            return
        channel = self._chat[channel_id]
        channel.topic = message

    def on_rename(self, nick: IrcNickWithMode, new_nick: IrcNickWithMode):
        for ch in self._chat.values():
            if nick.nick not in ch.chatters:
                continue
            chatter = ch.chatters[nick.nick]
            ch.chatters.remove(chatter)
            chatter.nick = new_nick.nick
            ch.chatters.add(chatter)

    def on_message(self, nick: IrcNickWithMode, target, text,
                   type_: MessageType):
        if self._chat_filter(nick.nick):
            return
        public_channel = ChannelID.public(target)
        if public_channel in self._chat:
            channel = self._chat[public_channel]
            self._on_public_msg(nick, channel, text, type_)
        elif target == self._irc.my_username.nick:
            self._on_private_msg(nick, text, type_)

    def _on_public_msg(self, nick: IrcNickWithMode, channel, text,
                       type_: MessageType):
        if nick.nick not in channel.chatters:
            return
        chatter = channel.chatters[nick.nick]
        line = ChatLine(chatter, text, type_)
        channel.lines.add(line)

    def _on_private_msg(self, nick: IrcNickWithMode, text, type_: MessageType):
        cid = ChannelID.private(nick.nick)
        self._add_channel(cid)
        channel = self._chat[cid]
        self._add_or_update_from_nick(channel, nick)
        self._add_or_update_from_nick(channel, self._irc.my_username)
        chatter = channel.chatters[nick.nick]
        line = ChatLine(chatter, text, type_)
        channel.lines.add(line)

    # Interface for player model updater.
    def on_player_added(self, player):
        name = player.login
        for channel in self._chat.values():
            if name in channel.chatters:
                ch = channel.chatters[name]
                ch.player = player

    def on_player_removed(self, player):
        name = player.login
        for channel in self._chat.values():
            if name in channel.chatters:
                ch = channel.chatters[name]
                ch.player = None

    # Interface for other stuff.
    def set_chat_filter(self, chat_filter):
        self._chat_filter = chat_filter
