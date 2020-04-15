import json


class LobbyProtocol:
    # TODO logging
    def __init__(self, connection):
        self._connection = connection
        self._consumers = {}
        connection.new_message.connect(self._handle)

    def register(self, command, callback):
        self._consumers[command] = callback

    def send(self, msg):
        self._connection.write(json.dumps(msg))

    def _handle(self, msg):
        if msg == "PING":
            self._connection.write("PONG")
            return

        try:
            msg = json.loads(msg)
        except json.JSONDecodeError:
            return

        if "command" not in msg:
            return
        cmd = msg['command']
        if cmd in self._consumers:
            self._consumers[cmd](msg)
