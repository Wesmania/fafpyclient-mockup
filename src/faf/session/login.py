import asyncio
from enum import Enum
from rx.subject import Subject, BehaviorSubject
from rx import operators as ops
from PySide2.QtCore import QObject, Signal, Slot

from faf.lobbyserver.connection import ConnectionState
from faf.lobbyserver.messages.login import AuthError
from faf.tools import unique_id


class LoginState(Enum):
    LOGGED_OUT = 0
    LOGGING_IN = 1
    LOGGED_IN = 2


class LoginProcess:
    def __init__(self, connection, login_message, unique_id):
        self._connection = connection
        self._unique_id = unique_id
        self._login_message = login_message
        self._login_task = None
        self.obs_state = BehaviorSubject(LoginState.LOGGED_OUT)
        self.obs_auth_results = Subject()
        self._connection.state_stream.subscribe(self._on_conn_state)

    @property
    def state(self):
        return self.obs_state.value

    @state.setter
    def state(self, val):
        return self.obs_state.on_next(val)

    @classmethod
    def build(cls, lobby_server):
        uid = unique_id.unique_id
        return cls(lobby_server.connection, lobby_server.login_msg, uid)

    def login(self, login, password):
        if self.state is not LoginState.LOGGED_OUT:
            return
        self.state = LoginState.LOGGING_IN
        task = self._perform_login(login, password)
        self._login_task = asyncio.get_event_loop().create_task(task)

    def logout(self):
        self._connection.disconnect_()

    async def _perform_login(self, login, password):
        self._connection.connect_()
        await self._connection.state_stream.pipe(
            ops.skip_while(lambda s: s is not ConnectionState.CONNECTED),
            ops.first()
        )
        try:
            result = await self._login_message.perform_login(login, password,
                                                             self._unique_id)
            self.obs_auth_results.on_next((True, result))
            self.state = LoginState.LOGGED_IN
        except AuthError as e:
            self.obs_auth_results.on_next((False, e.args[0]))    # TODO
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

        self.state = LoginState.LOGGED_OUT


class LobbyLogin(QObject):
    logged_in = Signal()
    logging_in = Signal()
    login_failed = Signal()
    logged_out = Signal()
    auth_error = Signal(str)

    def __init__(self, login_process, login_session):
        QObject.__init__(self)
        self._login_process = login_process
        self._login_session = login_session

        self._login_process.obs_state.pipe(
            ops.distinct_until_changed(),
            ops.pairwise()
        ).subscribe(self._on_login_state_change)
        self._login_process.obs_auth_results.subscribe(self._on_auth_results)

    @Slot(str, str)
    def login(self, login, password):
        self._login_process.login(login, password)

    @Slot()
    def logout(self):
        self._login_process.logout()

    def _on_login_state_change(self, states):
        old, new = states
        if new is LoginState.LOGGED_IN:
            self.logged_in.emit()
            return
        if new is LoginState.LOGGING_IN:
            self.logging_in.emit()
            return

        assert(new is LoginState.LOGGED_OUT)
        self._login_session.reset()

        if old is LoginState.LOGGED_IN:
            self.logged_out.emit()
        elif old is LoginState.LOGGING_IN:
            self.login_failed.emit()

    def _on_auth_results(self, results):
        success, msg = results
        if not success:
            self.auth_error.emit(msg)
        else:
            self._login_session.load_from_login_msg(msg)
