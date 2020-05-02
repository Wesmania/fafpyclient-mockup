from faf.models.data.channel import Channel, ChannelID
from faf.models.data.chatter import Chatter, IRCMode
from faf.models.data.chatline import ChatLine, ChatLineType
from faf.irc.ctcp import ctcp_dequote
from faf.irc.style import unstyle


# TODO - move some bits that have to do with irc format to irc module.
class ModelChatUpdater:
    def __init__(self, models, irc):
        self._models = models
        self._irc = irc
        self._chat_filter = lambda _: False

        self._irc.disconnected.connect(self.on_disconnect)
        self._irc.on('RPL_NAMREPLY', self.on_names)
        self._irc.on('JOIN', self.on_join)
        self._irc.on('QUIT', self.on_quit)
        self._irc.on('PART', self.on_part)
        self._irc.on('RPL_TOPIC', self.on_topic)
        self._irc.on('PRIVMSG', self.on_privmsg)
        self._irc.on('NOTICE', self.on_notice)
        self._irc.on('USERMODE', self.on_usermode)
        self._irc.on('NICK', self.on_rename)

    @property
    def _players(self):
        return self._models.players

    @property
    def _chat(self):
        return self._models.chat

    def _add_or_update_from_name(self, channel, name):
        stripped_name = IRCMode.strip(name)
        if stripped_name not in channel.chatters:
            new = Chatter.from_nick(name)
            if stripped_name in self._players:
                new.player = self._players[stripped_name]
            channel.chatters.add(new)
            channel.chatters.added.on_next(new)
        else:
            existing = channel.chatters[stripped_name]
            mode = IRCMode.from_nick(name)
            existing.mode = mode

    def _remove_from_name(self, channel, name):
        stripped_name = IRCMode.strip(name)
        if stripped_name not in channel.chatters:
            return
        to_remove = channel.chatters[stripped_name]
        channel.chatters.remove(to_remove)
        channel.chatters.removed.on_next(to_remove)

    def _remove_from_all(self, name):
        for channel in self._chat.values():
            self._remove_from_name(channel, name)

    def _update_mode(self, channel, stripped_name, modes):
        if stripped_name not in channel.chatters:
            return
        chatter = channel.chatters[stripped_name]
        new_mode = IRCMode.from_usermode(chatter.mode, modes)
        chatter.mode = new_mode

    def _add_channel(self, id_):
        if id_ in self._chat:
            return
        ch = Channel(id_)
        self._chat.add(ch)
        self._chat.added.on_next(ch)

    def _remove_channel(self, id_):
        if id_ not in self._chat:
            return
        ch = self._chat[id_]
        self._chat.remove(ch)
        self._chat.removed.on_next(ch)

    def on_disconnect(self, **kwargs):
        # FIXME - for persisting channel contents we'll want to emit a list of
        # removed channels here
        self._chat.clear()
        self._chat.cleared.on_next(None)

    def on_names(self, channel_name, users, **kwargs):
        channel_id = ChannelID.public(channel_name)
        if channel_id not in self._chat:
            return
        channel = self._chat[channel_id]
        for name in users:
            self._add_or_update_from_name(channel, name)

    def on_join(self, channel_name, nick=None, **kwargs):
        if nick is None:
            return
        channel_id = ChannelID.public(channel_name)
        if nick == self._irc.my_username:
            self._add_channel(channel_id)

        if channel_id not in self._chat:
            return
        channel = self._chat[channel_id]
        self._add_or_update_from_name(channel, nick)

    def on_part(self, channel_name, message, nick=None, **kwargs):
        if nick is None:
            return
        channel_id = ChannelID.public(channel_name)
        if channel_id not in self._chat:
            return
        channel = self._chat[channel_id]
        self._remove_from_name(channel, nick)

        if nick == self._irc.my_username:
            self._remove_channel(channel_id)

    def on_quit(self, message, nick=None, **kwargs):
        if nick is None:
            return
        self._remove_from_all(nick)

    def on_usermode(self, nick, modes, **kwargs):
        stripped_name = IRCMode.strip(nick)
        for channel in self._chat.values():
            self._update_mode(channel, stripped_name, modes)

    def on_topic(self, channel, message, **kwargs):
        channel_id = ChannelID.public(channel)
        if channel_id not in self._chat:
            return
        channel = self._chat[channel_id]
        channel.topic = message

    def on_rename(self, new_nick, nick=None, **kwargs):
        if nick is None:
            return
        nick = IRCMode.strip(nick)
        new_nick = IRCMode.strip(new_nick)
        for ch in self._chat.values():
            if nick not in ch.chatters:
                continue
            chatter = ch.chatters[nick]
            ch.chatters.remove(chatter)
            chatter.nick = new_nick
            ch.chatters.add(chatter)

    def on_privmsg(self, target, message, nick=None, **kwargs):
        if nick is None:
            return
        nick = IRCMode.strip(nick)
        if self._chat_filter(nick):
            return
        messages = ctcp_dequote(message)
        for msg in messages:
            if isinstance(msg, tuple):
                self._on_action(nick, target, msg, **kwargs)
            else:
                self._on_msg(nick, target, msg, ChatLineType.MESSAGE)

    def on_notice(self, target, message, nick=None, **kwargs):
        if nick is None:
            return
        nick = IRCMode.strip(nick)
        if self._chat_filter(nick):
            return
        self._on_msg(nick, target, message, ChatLineType.NOTICE)

    def _on_action(self, nick, target, message, **kwargs):
        if message[0] != 'ACTION':
            return
        if len(message) < 2:
            return
        self._on_msg(nick, target, message[1], ChatLineType.ACTION)

    def _on_msg(self, nick, target, text, type_):
        public_channel = ChannelID.public(target)
        if public_channel in self._chat:
            channel = self._chat[public_channel]
            self._on_public_msg(nick, channel, text, type_)
        elif target == self._irc.my_username:
            self._on_private_msg(nick, text, type_)

    def _on_public_msg(self, nick, channel, text, type_):
        if nick not in channel.chatters:
            return
        chatter = channel.chatters[nick]
        line = ChatLine(chatter, unstyle(text), type_)
        channel.lines.add(line)

    def _on_private_msg(self, nick, text, type_):
        cid = ChannelID.private(nick)
        self._add_channel(cid)
        channel = self._chat[cid]
        self._add_or_update_from_name(channel, nick)
        self._add_or_update_from_name(channel, self._irc.my_username)
        chatter = channel.chatters[nick]
        line = ChatLine(chatter, unstyle(text), type_)
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
