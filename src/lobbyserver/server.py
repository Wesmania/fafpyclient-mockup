from lobbyserver.connection import LobbyConnection
from lobbyserver.protocol import LobbyProtocol
from lobbyserver.login import LobbyLogin
from lobbyserver.messages.games import GameMessage
from lobbyserver.messages.players import PlayerMessage


class LobbyServer:
    def __init__(self, host, port):
        self.connection = LobbyConnection(host, port)
        self.protocol = LobbyProtocol(self.connection)
        self.login = LobbyLogin.build(self.connection, self.protocol)
        self.game_msg = GameMessage(self.protocol)
        self.player_msg = PlayerMessage(self.protocol)
