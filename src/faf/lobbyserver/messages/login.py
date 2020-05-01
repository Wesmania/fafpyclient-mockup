import hashlib
from dataclasses import dataclass


def mangle_password(password):
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()


@dataclass
class LoginResult:
    login: str
    session: str
    unique_id: str
    player_info: dict


class AuthError(ConnectionError):
    pass


class LoginMessage:
    def __init__(self, lobby_protocol):
        self._messages = lobby_protocol.register(
            "welcome", "session", "authentication_failed")

    async def perform_login(self, login, password, unique_id):
        self._send_ask_session()
        msg_type, msg = await self._messages
        if msg_type != "session":
            raise ConnectionError(f"Expected 'session', got {msg_type}")

        session = msg['session']
        password = mangle_password(password)
        self._send_hello(session, login, password, unique_id)
        msg_type, msg = await self._messages
        if msg_type not in ['welcome', 'authentication_failed']:
            raise ConnectionError(f"Expected auth message, got {msg_type}")

        if msg_type == 'welcome':
            player_info, login = msg["me"], msg["id"]
            return LoginResult(login, session, unique_id, player_info)
        else:
            raise AuthError(msg['text'])
