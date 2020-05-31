from rx.subject import Subject, BehaviorSubject
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
        pinfo = {
            'id': 6579,
            'login': 'foobar',
            'global_rating': [1500.00, 500.00],
            'ladder_rating': [1500.00, 500.00],
            'number_of_games': 1000,
            'avatar': {
                'url': 'https://todo.png',
                'tooltip': 'The FooBar'
            },
            'country': 'PL',
            'clan': 'SNF'
        }
        return LoginResult(login, password, "foo_session", 100, pinfo)


class MockLobbyServer:
    def __init__(self):
        self.game_msg = MockMessage()
        self.player_msg = MockMessage()
        self.login_msg = MockLoginMessage()
        self.obs_connection_state = BehaviorSubject(
            ConnectionState.DISCONNECTED)

    @property
    def connection_state(self):
        return self.obs_connection_state.value

    def connect(self):
        QTimer.singleShot(0, self._set_connected)

    def disconnect(self):
        QTimer.singleShot(0, self._set_disconnected)

    def _set_connected(self):
        self.obs_connection_state.on_next(ConnectionState.CONNECTING)
        self.obs_connection_state.on_next(ConnectionState.CONNECTED)

    def _set_disconnected(self):
        self.obs_connection_state.on_next(ConnectionState.DISCONNECTED)
