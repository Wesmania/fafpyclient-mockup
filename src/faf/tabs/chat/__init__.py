from PySide2.QtCore import QObject, Slot

from faf.tabs.games.gamemodel import LobbyGamesModel
from faf.tabs.chat.qt_models import ChatQtModel


class ChatTab(QObject):
    def __init__(self, models, qml_context):
        QObject.__init__(self)

        self.chat_qt_model = ChatQtModel(models.data.chat)
        self.lobby_game_model = LobbyGamesModel(models.qt.games)
        qml_context.setContextProperty("faf__tabs__chat__model",
                                       self.chat_qt_model)
        qml_context.setContextProperty("faf__tabs__chat", self)

    @Slot(str, bool)
    def leave_channel(self, channel_name, is_public):
        print(f"TODO: leave {channel_name}")

    @Slot(str, bool, str)
    def send_message(self, channel_name, is_public, message):
        print(f"TODO: send '{message}' to {channel_name}")
