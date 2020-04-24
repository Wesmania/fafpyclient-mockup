import hashlib
from enum import Enum

from PySide2.QtCore import QObject, Signal


def mangle_password(password):
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()


class _Requests(Enum):
    START = 0
    ABORT = 1


class LoginMessage(QObject):
    logged_in = Signal(object)
    auth_failed = Signal(str)

    def __init__(self, protocol, unique_id):
        QObject.__init__(self)
        self._unique_id = unique_id
        self._protocol = protocol
        messages = protocol.register(
            "welcome", "session", "authentication_failed")
        messages.subscribe(self._handle_messages)

        self._creds = None
        self._session = None
        self._password = None
        self._uid = None

    def start(self, login, password):
        self._creds = (login, password)
        self._send_ask_session()

    def reset(self):
        self._creds = None
        self._password = None
        self._session = None
        self._uid = None

    def _handle_messages(self, msgs):
        kind, msg = msgs
        if kind == "session":
            self._session = str(msg["session"])
            self._send_hello()
        if kind == "welcome":
            id_, login = msg["id"], msg["login"]
            self.logged_in.emit((id_, login, self._session, self._uid))
        if kind == "authentication_failed":
            self.auth_failed.emit()

    def _send_ask_session(self):
        msg = {
            "command": "ask_session",
            "version": "0.18.9",
            "user_agent": "downlords-faf-client"
        }
        self._protocol.send(msg)

    def _send_hello(self):
        if self._creds is None:
            return

        login, password = self._creds
        password = mangle_password(password)
        self._uid = self._unique_id(login, self._session)
        msg = {
            "command": "hello",
            "login": login,
            "password": password,
            "unique_id": self._uid,
            "session": self._session
        }
        self._protocol.send(msg)
