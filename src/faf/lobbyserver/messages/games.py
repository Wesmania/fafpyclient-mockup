from rx import operators as ops
from rx.scheduler.mainloop import QtScheduler
from rx.scheduler import ImmediateScheduler
from PySide2 import QtCore
from faf.models.data.game import GameVisibility, GameState


class GameMessage:
    def __init__(self, protocol):
        # See comment in players.py.
        self._aio_scheduler = QtScheduler(QtCore)
        messages = protocol.register("game_info")
        self.new = messages.pipe(
            ops.flat_map(self._split_game_info),
            ops.observe_on(self._aio_scheduler),
            ops.flat_map(self._process_game),
            ops.observe_on(ImmediateScheduler()),
            ops.filter(lambda x: x is not None),
        )

    def _split_game_info(self, msgs):
        cmd, msg = msgs
        if "games" in msg:
            games = msg["games"]
            for i in range(0, len(games), 10):
                yield games[i:i+10]
        else:
            yield [msg]

    def _process_game(self, msgs):
        for msg in msgs:
            try:
                msg["state"] = GameState(msg["state"])
                msg["visibility"] = GameVisibility(msg["visibility"])
                yield msg
            except (KeyError, ValueError):
                pass
