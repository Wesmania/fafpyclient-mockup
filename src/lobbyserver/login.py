from enum import Enum
from PySide2.QtCore import QObject, Signal, Slot

from lobbyserver.connection import ConnectionState
from lobbyserver.messages.login import LoginMessage
from tools import unique_id


class LoginState(Enum):
    LOGGED_OUT = 0
    LOGGING_IN = 1
    LOGGED_IN = 2


class LobbyLogin(QObject):
    logged_in = Signal(object)
    logged_out = Signal()
    auth_failed = Signal(str)

    def __init__(self, connection, login_message):
        QObject.__init__(self)
        self._connection = connection
        self._login_message = login_message
        self._creds = None

        self.state = LoginState.LOGGED_OUT
        connection.state_stream.subscribe(self._on_connection)
        login_message.logged_in.connect(self._on_logged_in)
        login_message.auth_failed.connect(self._on_auth_failed)

    @classmethod
    def build(cls, connection, protocol):
        uid = unique_id.unique_id
        login_message = LoginMessage(protocol, uid)
        return cls(connection, login_message)

    @Slot(str, str)
    def login(self, login, password):
        if self.state is not LoginState.LOGGED_OUT:
            return
        self._creds = (login, password)
        self._connection.connect_()
        self.state = LoginState.LOGGING_IN

    @Slot()
    def logout(self):
        self._connection.disconnect_()

    def _on_connection(self, state):
        if state is ConnectionState.DISCONNECTED:
            self._login_message.reset()
            if self.state is not LoginState.LOGGED_OUT:
                self.state = LoginState.LOGGED_OUT
                self.logged_out.emit()
        elif state is ConnectionState.CONNECTED:
            self._login_message.start(*self._creds)

    def _on_logged_in(self, creds):
        self.state = LoginState.LOGGED_IN
        self.logged_in.emit(creds)

    def _on_auth_failed(self, msg):
        self.auth_failed.emit(msg)
        self.logout()
