from models.data.game import Game, GameState


class ModelGameUpdater:
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

    def add_or_update_game(self, gid, *args, **kwargs):
        if gid in self._games:
            return self._add_game(gid, *args, **kwargs)
        else:
            return self._update_game(gid, *args, **kwargs)

    def _update_players(self, pids, game):
        changed_pids = []
        for pid in game.players:
            if self._current_player_game.set_player_game(pid, game):
                changed_pids.append(pid)
        return changed_pids

    def _emit_players(self, pids, game):
        for pid in pids:
            if pid not in self._players:
                continue
            self._players.obs_game.on_next(game)

    def _add_game(self, gid, attrs):
        game = Game(gid)
        game.update(attrs)
        if game.state is GameState.CLOSED:
            return

        self._games.add(game)
        changed_pids = self._update_players(game.players, game)

        self._games.added.on_next(game)
        self._emit_players(changed_pids, game)

    def _update_game(self, gid, attrs):
        game = self._games[gid]
        old_player_ids = game.players
        game.update(attrs)
        player_ids = game.players

        pdiff = player_ids ^ old_player_ids
        changed_pids = self._update_players(pdiff, game)
        self._emit_players(changed_pids, game)

        if game.state is GameState.CLOSED:
            self.remove_game(game.id)

    def remove_game(self, gid):
        if gid not in self._games:
            return
        game = self._games[gid]
        changed_pids = self._update_players(game.players, None)

        self._games.removed.on_next(game)
        self._emit_players(changed_pids, game)
        game.complete()
