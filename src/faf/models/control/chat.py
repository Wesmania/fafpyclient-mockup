from faf.models.data.channel import Channel, ChannelID
from faf.models.data.chatter import Chatter, IRCMode


class ModelChatUpdater:
    def __init__(self, models, irc):
        self._models = models
        self._irc = irc

        self._irc.on('CLIENT_DISCONNECT', self.on_disconnect)
        self._irc.on('RPL_NAMREPLY', self.on_names)
        self._irc.on('JOIN', self.on_join)
        self._irc.on('QUIT', self.on_quit)
        self._irc.on('PART', self.on_part)
        self._irc.on('RPL_TOPIC', self.on_topic)
        self._irc.on('MESSAGE', self.on_message)
        self._irc.on('PRIVMSG', self.on_privmsg)
        self._irc.on('ACTION', self.on_action)
        self._irc.on('USERMODE', self.on_usermode)

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
        for channel in self._chat:
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

    def on_names(self, channel, users, **kwargs):
        channel = ChannelID.public(channel)
        if channel not in self._chat:
            return
        channel = self._chat[channel]
        for name in users:
            self._add_or_update_from_name(channel, name)

    def on_join(self, nick, channel, **kwargs):
        channel = ChannelID.public(channel)
        if nick == self._irc.my_username:
            self._add_channel(channel)

        if channel not in self._chat:
            return
        channel = self._chat[channel]
        self._add_or_update_from_name(channel, nick)

    def on_part(self, nick, channel, message, **kwargs):
        channel_id = ChannelID.public(channel)
        if channel_id not in self._chat:
            return
        channel = self._chat[channel_id]
        self._remove_from_name(channel, nick)

        if nick == self._irc.my_username:
            self._remove_channel(channel_id)

    def on_quit(self, nick, message, **kwargs):
        self._remove_from_all(nick)

    def on_usermode(self, nick, modes, **kwargs):
        stripped_name = IRCMode.strip(nick)
        for channel in self._chat:
            self._update_mode(channel, stripped_name, modes)

    def on_topic(self, channel, message, **kwargs):
        channel_id = ChannelID.public(channel)
        if channel_id not in self._chat:
            return
        channel = self._chat[channel_id]
        channel.topic = message

    # TODO - on rename

    def on_message(self, **kwargs):
        # TODO
        pass

    def on_privmsg(self, **kwargs):
        # TODO
        pass

    def on_action(self, **kwargs):
        # TODO
        pass

    def on_player_added(self, player):
        name = player.login
        for channel in self._chat:
            if name in channel.chatters:
                ch = channel.chatters[name]
                ch.player = player

    def on_player_removed(self, player):
        name = player.login
        for channel in self._chat:
            if name in channel.chatters:
                ch = channel.chatters[name]
                ch.player = None
