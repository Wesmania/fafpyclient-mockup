from models.data.player import Player


class ModelPlayerUpdater:
    def __init__(self, models, player_msg):
        self._models = models
        player_msg.new.subscribe(self._on_player_msg)

    @property
    def _players(self):
        return self._models.players

    @property
    def _games(self):
        return self._models.games

    @property
    def _current_player_game(self):
        return self._models.current_player_game

    def _on_player_msg(self, msg):
        self.add_or_update_player(msg["id"], msg)

    def add_or_update_player(self, pid, attrs):
        if pid not in self._games:
            return self._add_player(pid, attrs)
        else:
            return self._update_player(pid, attrs)

    def _add_player(self, pid, attrs):
        player = Player(self._current_player_game, pid)
        player.update(attrs)
        self._players.add(player)
        self._players.added.on_next(player)

    def _update_player(self, pid, attrs):
        if pid not in self._players:
            return
        player = self._players[pid]
        player.update(attrs)

    def remove_player(self, pid):
        if pid not in self._players:
            return
        player = self._players[pid]
        self._players.remove(player)
        self._players.removed.on_next(player)
        player.complete()
