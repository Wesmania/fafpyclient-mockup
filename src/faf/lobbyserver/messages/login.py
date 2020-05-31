import hashlib
from dataclasses import dataclass
from rx import operators as ops


def mangle_password(password):
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()


@dataclass
class LoginResult:
    login: str
    password: str
    session: str
    unique_id: str
    player_info: dict


class AuthError(ConnectionError):
    pass


class LoginMessage:
    def __init__(self, lobby_protocol, tools):
        self._lobby_protocol = lobby_protocol
        self._tools = tools
        self._messages = lobby_protocol.register(
            "welcome", "session", "authentication_failed")

    async def perform_login(self, login, password):
        msg_type, msg = await self._send_ask_session()
        if msg_type != "session":
            raise ConnectionError(f"Expected 'session', got {msg_type}")

        session = str(msg['session'])
        unique_id = self._tools.unique_id(session)
        password = mangle_password(password)
        msg_type, msg = await self._send_hello(login, password, unique_id,
                                               session)
        if msg_type not in ['welcome', 'authentication_failed']:
            raise ConnectionError(f"Expected auth message, got {msg_type}")

        if msg_type == 'welcome':
            player_info, login = msg["me"], msg["id"]
            print(session, unique_id, player_info)
            return LoginResult(login, password, session, unique_id,
                               player_info)
        else:
            raise AuthError(msg['text'])

    def _next_msg(self):
        return self._messages.pipe(ops.first())

    def _send_ask_session(self):
        msg = {
            "command": "ask_session",
            "version": "0.18.9",
            "user_agent": "downlords-faf-client"
        }
        self._lobby_protocol.send(msg)
        return self._next_msg()

    def _send_hello(self, login, password, unique_id, session):
        msg = {
            "command": "hello",
            "login": login,
            "password": password,
            "unique_id": unique_id,
            "session": session
        }
        self._lobby_protocol.send(msg)
        return self._next_msg()
