from models.data.player import Player


class ModelPlayerUpdater:
    def __init__(self, models):
        self._models = models

    @property
    def _players(self):
        return self._models.players

    @property
    def _games(self):
        return self._models.games

    @property
    def _current_player_game(self):
        return self._models.current_player_game

    def add_or_update_player(self, pid, attrs):
        if pid in self._games:
            return self._add_player(pid, attrs)
        else:
            return self._update_player(pid, attrs)

    def _add_player(self, pid, attrs):
        player = Player(self._games, self._game_player_relation, pid)
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
