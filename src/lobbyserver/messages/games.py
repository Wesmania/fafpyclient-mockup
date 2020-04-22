from rx import operators as ops
from models.data.game import GameVisibility, GameState


class GameMessage:
    def __init__(self, protocol):
        messages = protocol.register("game_info")
        self.new = messages.pipe(
            ops.flat_map(self._handle_game_info),
            ops.map(self._process_game),
            ops.filter(lambda x: x is not None),
        )

    # TODO validate
    def _handle_game_info(self, msgs):
        cmd, msg = msgs
        if "games" in msg:
            return msg["games"]
        else:
            return [msg]

    def _process_game(self, msg):
        try:
            msg["state"] = GameState(msg["state"])
            msg["visibility"] = GameVisibility(msg["visibility"])
            return msg
        except (KeyError, ValueError):
            return None
