from enum import Enum
import asyncio
from PySide2.QtCore import QObject, Signal, Slot

from faf.lobbyserver.connection import ConnectionState
from faf.lobbyserver.messages import LoginMessage
from faf.lobbyserver.messages.login import AuthError
from faf.tools import unique_id


class LoginState(Enum):
    LOGGED_OUT = 0
    LOGGING_IN = 1
    LOGGED_IN = 2


class LobbySession:
    def __init__(self):
        self.username = None
        self.player = None


class LobbyLogin(QObject):
    logged_in = Signal(object)
    logging_in = Signal()
    login_failed = Signal()
    logged_out = Signal()
    auth_error = Signal(str)

    def __init__(self, connection, unique_id, login_message):
        QObject.__init__(self)
        self._connection = connection
        self._unique_id = unique_id
        self._login_message = login_message
        self._login_task = None
        self._user_creds = None

        self.creds = None
        self.logout_msg = ""
        self.state = LoginState.LOGGED_OUT

        connection.state_stream.subscribe(self._on_conn_state)

    @classmethod
    def build(cls, connection, protocol):
        uid = unique_id.unique_id
        login_message = LoginMessage(protocol)
        return cls(connection, uid, login_message)

    @Slot(str, str)
    def login(self, login, password):
        if self.state is not LoginState.LOGGED_OUT:
            return
        self.state = LoginState.LOGGING_IN
        self.logging_in.emit()
        task = self._perform_login(login, password)
        self._login_task = asyncio.get_event_loop().create_task(task)

    @Slot()
    def logout(self):
        self._connection.disconnect_()

    async def _perform_login(self, login, password):
        self._connection.connect_()
        conn_state = self._connection.state
        while conn_state is not ConnectionState.CONNECTED:
            conn_state = await self._connection.state_stream
        try:
            unique_id = self._unique_id(login)
            result = await self._login_message.perform_login(login, password,
                                                             unique_id)
            self.state = LoginState.LOGGED_IN
            self.logged_in.emit(result)
        except AuthError as e:
            self.auth_error.emit(e.args[0])    # TODO
            self._connection.disconnect()
        except ConnectionError:
            self._connection.disconnect()

    def _on_conn_state(self, state):
        if self.state is LoginState.LOGGED_OUT:
            return
        if state is not ConnectionState.DISCONNECTED:
            return

        if self._login_task is not None:
            if not self._login_task.done():
                self._login_task.cancel()
            self._login_task = None

        old, self.state = self.state, LoginState.LOGGED_OUT
        if old is LoginState.LOGGED:
            self.logged_out.emit()
        else:
            self.login_failed.emit()
