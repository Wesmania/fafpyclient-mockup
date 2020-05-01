from faf.lobbyserver.connection import LobbyConnection
from faf.lobbyserver.protocol import LobbyProtocol
from faf.lobbyserver.messages import GameMessage, PlayerMessage, LoginMessage


class LobbyServer:
    def __init__(self, host, port):
        self.connection = LobbyConnection(host, port)
        self.protocol = LobbyProtocol(self.connection)
        self.game_msg = GameMessage(self.protocol)
        self.player_msg = PlayerMessage(self.protocol)
        self.login_msg = LoginMessage(self.protocol)
