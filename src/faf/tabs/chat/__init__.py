from PySide2.QtCore import QObject, Slot

from faf.tabs.chat.qt_models import ChatQtModel
from faf.tabs.chat.control import IrcControl, IrcLineParser


class ChatTab(QObject):
    def __init__(self, irc, models, qml_context):
        QObject.__init__(self)

        self._irc = irc
        self.irc_control = IrcControl(self._irc.client,
                                      models.control.chat_updater)
        self.irc_parser = IrcLineParser(self.irc_control)
        self.chat_qt_model = ChatQtModel(models.data.chat)

        qml_context.setContextProperty("faf__tabs__chat__model",
                                       self.chat_qt_model)
        qml_context.setContextProperty("faf__tabs__chat", self)

    @Slot(str, bool)
    def leave_channel(self, channel_name, is_public):
        self.irc_control.part(channel_name, is_public)

    @Slot(str, bool, str)
    def send_message(self, channel_name, is_public, message):
        self.irc_parser.handle_line(channel_name, message)
