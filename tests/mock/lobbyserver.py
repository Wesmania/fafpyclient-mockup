from rx.subject import Subject
from PySide2.QtCore import QTimer

from faf.lobbyserver.messages.login import LoginResult
from faf.lobbyserver.connection import ConnectionState


class MockMessage:
    def __init__(self):
        self.new = Subject()


class MockLoginMessage:
    def __init__(self):
        pass

    async def perform_login(self, login, password):
        return LoginResult(login, password, "foo_session", "foo_id",
                           "foo_session")


class MockLobbyServer:
    def __init__(self):
        self.game_msg = MockMessage()
        self.player_msg = MockMessage()
        self.login_msg = MockLoginMessage()
        self.obs_connection_state = Subject(ConnectionState.DISCONNECTED)

    @property
    def connection_state(self):
        return self.obs_connection_state.value

    def connect(self):
        QTimer.singleShot(0, self, self._set_connected)

    def disconnect(self):
        QTimer.singleShot(0, self, self._set_disconnected)

    def _set_connected(self):
        self.obs_connection_state.on_next(ConnectionState.CONNECTING)
        self.obs_connection_state.on_next(ConnectionState.CONNECTED)

    def _set_disconnected(self):
        self.obs_connection_state.on_next(ConnectionState.DISCONNECTED)
