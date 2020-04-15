from lobbyserver.connection import LobbyConnection
from lobbyserver.protocol import LobbyProtocol
from lobbyserver.login import LobbyLogin


class LobbyServer:
    def __init__(self, connection, protocol, login):
        self.connection = connection
        self.protocol = protocol
        self.login = login

    @classmethod
    def build(cls, host, port):
        connection = LobbyConnection(host, port)
        protocol = LobbyProtocol(connection)
        login = LobbyLogin.build(connection, protocol)
        return cls(connection, protocol, login)
