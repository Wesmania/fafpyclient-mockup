from models.data.game import Game, GameState


class ModelGameUpdater:
    def __init__(self, models, game_msg):
        self._models = models
        game_msg.new.subscribe(self._on_game_msg)

    @property
    def _players(self):
        return self._models.players

    @property
    def _games(self):
        return self._models.games

    @property
    def _current_player_game(self):
        return self._models.current_player_game

    def _on_game_msg(self, msg):
        self.add_or_update_game(msg["uid"], msg)

    def add_or_update_game(self, gid, *args, **kwargs):
        if gid not in self._games:
            return self._add_game(gid, *args, **kwargs)
        else:
            return self._update_game(gid, *args, **kwargs)

    def _emit_players(self, pids, game):
        for pid in pids:
            if pid not in self._players:
                continue
            self._players[pid].obs_game.on_next(game)

    def _add_game(self, gid, attrs):
        game = Game(gid)
        game.update(attrs)
        if game.state is GameState.CLOSED:
            return

        self._games.add(game)
        pids = self._current_player_game.add_players(game.players, game)
        self._games.added.on_next(game)
        self._emit_players(pids, game)

    def _update_game(self, gid, attrs):
        game = self._games[gid]
        old_player_ids = game.players
        game.update(attrs)
        player_ids = game.players

        new_players = player_ids - old_player_ids
        old_players = old_player_ids - player_ids
        pids = self._current_player_game.add_players(new_players, game)
        pids += self._current_player_game.remove_players(old_players, game)
        self._emit_players(pids, game)

        if game.state is GameState.CLOSED:
            self.remove_game(game.id)

    def remove_game(self, gid):
        if gid not in self._games:
            return
        game = self._games[gid]
        pids = self._current_player_game.remove_players(game.players, game)
        self._games.remove(game)

        self._games.removed.on_next(game)
        self._emit_players(pids, game)
        game.complete()
