from faf.lobbyserver.connection import LobbyConnection
from faf.lobbyserver.protocol import LobbyProtocol
from faf.lobbyserver.messages import GameMessage, PlayerMessage, LoginMessage


class LobbyServer:
    def __init__(self, config, tools):
        self._connection = LobbyConnection(config["host"], config["port"])
        self._protocol = LobbyProtocol(self._connection)
        self.game_msg = GameMessage(self._protocol)
        self.player_msg = PlayerMessage(self._protocol)
        self.login_msg = LoginMessage(self._protocol, tools)

    @property
    def obs_connection_state(self):
        return self._connection.obs_state

    @property
    def connection_state(self):
        return self.obs_connection_state.value

    def connect(self):
        self._connection.connect_()

    def disconnect(self):
        self._connection.disconnect_()
