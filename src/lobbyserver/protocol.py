import json
from rx import operators as ops


class LobbyProtocol:
    # TODO logging
    def __init__(self, connection):
        self._connection = connection
        self.message_stream = self._connection.message_stream.pipe(
            ops.filter(self._handle_ping),
            ops.map(self._parse_cmd),
            ops.filter(lambda x: x is not None),
        )

    def register(self, *commands):
        return self.message_stream.pipe(
            ops.filter(lambda m: m[0] in commands)
        )

    def send(self, msg):
        self._connection.write(json.dumps(msg))

    def _handle_ping(self, msg):
        if msg == "PING":
            self._connection.write("PONG")
            return False
        return True

    def _parse_cmd(self, msg):
        try:
            msg = json.loads(msg)
        except json.JSONDecodeError:
            return None
        if "command" not in msg:
            return None
        return (msg["command"], msg)
