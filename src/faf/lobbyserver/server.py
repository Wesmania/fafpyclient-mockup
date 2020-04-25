from faf.lobbyserver.connection import LobbyConnection
from faf.lobbyserver.protocol import LobbyProtocol
from faf.lobbyserver.login import LobbyLogin
from faf.lobbyserver.messages import GameMessage, PlayerMessage


class LobbyServer:
    def __init__(self, host, port, qml_context):
        self.connection = LobbyConnection(host, port)
        self.protocol = LobbyProtocol(self.connection)
        self.login = LobbyLogin.build(self.connection, self.protocol)
        self.game_msg = GameMessage(self.protocol)
        self.player_msg = PlayerMessage(self.protocol)

        qml_context.setContextProperty("faf__server__login", self.login)
