import hashlib
from enum import Enum
from PySide2.QtCore import QObject, Signal


def mangle_password(password):
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()


class _MsgState(Enum):
    AWAITING_CREDS = 0
    AWAITING_SESSION = 1
    AWAITING_WELCOME = 2
    DONE = 3


class LoginMessage(QObject):
    logged_in = Signal(object)
    auth_failed = Signal()

    def __init__(self, protocol, unique_id):
        QObject.__init__(self)
        self._unique_id = unique_id
        self._protocol = protocol
        self._protocol.register("welcome", self._handle_welcome)
        self._protocol.register("session", self._handle_session)
        self._protocol.register("authentication_failed",
                                self._handle_auth_failed)

        self._state = _MsgState.DONE
        self._creds = None
        self._session = None
        self._password = None
        self._uid = None

    def reset(self):
        self._state = _MsgState.DONE
        self._creds = None
        self._password = None
        self._session = None
        self._uid = None

    def set_creds(self, login, password):
        password = mangle_password(password)
        self._creds = (login, password)

    def start_login(self):
        if self._creds is None or self._state is not _MsgState.DONE:
            raise ValueError
        self._send_ask_session()
        self._state = _MsgState.AWAITING_SESSION

    def _send_ask_session(self):
        msg = {
            "command": "ask_session",
            "version": "0.18.9",
            "user_agent": "downlords-faf-client"
        }
        self._protocol.send(msg)

    # TODO validation (voluptuous looks nice)
    def _handle_session(self, msg):
        if self._state is not _MsgState.AWAITING_SESSION:
            return
        self._session = str(msg["session"])
        self._send_hello()
        self._state = _MsgState.AWAITING_WELCOME

    def _send_hello(self):
        login, password = self._creds
        self._uid = self._unique_id(login, self._session)
        msg = {
            "command": "hello",
            "login": login,
            "password": password,
            "unique_id": self._uid,
            "session": self._session
        }
        self._protocol.send(msg)

    def _handle_welcome(self, msg):
        if self._state is not _MsgState.AWAITING_WELCOME:
            return
        id_, login = msg["id"], msg["login"]
        self.logged_in.emit((id_, login, self._session, self._uid))
        self._state = _MsgState.DONE

    def _handle_auth_failed(self, msg):
        if self._state is not _MsgState.AWAITING_WELCOME:
            return
        print("Auth failed")
        self.auth_failed.emit()
        self._state = _MsgState.DONE
