from rx import operators as ops
from rx.scheduler.mainloop import QtScheduler
from rx.scheduler import ImmediateScheduler
from PySide2 import QtCore


class PlayerMessage:
    def __init__(self, protocol):
        # We use this scheduler so that we don't handle all player messages at
        # the same time at startup, as this hangs the UI for a few seconds.
        # With this, it's just a minor slowdown.
        #
        # One side effect is that games and players don't appear immediately
        # (as in, UI is available before they're all shown). This shouldn't be
        # a problem.
        self._aio_scheduler = QtScheduler(QtCore)
        messages = protocol.register("player_info")
        self.new = messages.pipe(
            ops.flat_map(self._split_player_info),
            ops.observe_on(self._aio_scheduler),
            ops.flat_map(self._handle_player_info),
            ops.observe_on(ImmediateScheduler()),
        )

    def _split_player_info(self, msgs):
        cmd, msg = msgs
        players = msg["players"]
        for i in range(0, len(players), 10):
            yield players[i:i+10]

    # TODO validate
    def _handle_player_info(self, players):
        for player in players:
            player["id"] = int(player["id"])
        return players
