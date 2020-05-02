from dataclasses import dataclass
from PySide2.QtCore import Qt

from faf.qt import InternalModelQtProxy, QtRoleEnum
from faf.models.data.channel import ChannelType
from faf.tabs.chat.qt_models.chatters import ChattersQtModel, \
    ChattersQtFilterModel
from faf.tabs.chat.qt_models.chat_lines import ChatLineQtModel


@dataclass
class ChannelQtModels:
    raw_chatters: ChattersQtModel
    chatters: ChattersQtFilterModel
    lines: ChatLineQtModel


def make_qt_models(channel):
    raw_chatters = ChattersQtModel(channel.chatters)
    chatters = ChattersQtFilterModel(raw_chatters)
    lines = ChatLineQtModel(channel.lines)
    return ChannelQtModels(raw_chatters, chatters, lines)


class ChannelRoles(QtRoleEnum):
    channel_name = ()
    is_public = ()
    channel_topic = ()
    lines_model = ()
    chatters_model = ()


class ChatQtModel(InternalModelQtProxy):
    def __init__(self, chat):
        InternalModelQtProxy.__init__(self, chat)
        self._channel_models = {}

        self._update_roles_at(lambda c: c.obs_topic,
                              ChannelRoles.channel_topic)

    def _add_item(self, item):
        self._channel_models[item.id_key] = make_qt_models(item)
        InternalModelQtProxy._add_item(self, item)

    def _remove_item(self, item):
        InternalModelQtProxy._remove_item(self, item)
        del self._channel_models[item.id_key]

    def _clear_items(self, _):
        InternalModelQtProxy._remove_item(self, _)
        self._channel_models.clear()

    def roleNames(self):
        return ChannelRoles.role_names()

    def role(self, channel, role):
        if role < Qt.UserRole or role >= len(ChannelRoles) + Qt.UserRole:
            return None
        role = ChannelRoles(role)
        if role is ChannelRoles.channel_name:
            return channel.id.name
        if role is ChannelRoles.is_public:
            return channel.id.type is ChannelType.PUBLIC
        if role is ChannelRoles.channel_topic:
            return channel.topic
        if role is ChannelRoles.chatters_model:
            return self._channel_models[channel.id_key].chatters
        if role is ChannelRoles.lines_model:
            return self._channel_models[channel.id_key].lines
