from rx import operators as ops


class PlayerMessage:
    def __init__(self, protocol):
        messages = protocol.register("player_info")
        self.new = messages.pipe(
            ops.flat_map(self._handle_player_info),
            ops.filter(lambda x: x is not None)
        )

    # TODO validate
    def _handle_player_info(self, msgs):
        cmd, msg = msgs
        players = msg["players"]
        for player in players:
            player["id"] = int(player["id"])
        return players
