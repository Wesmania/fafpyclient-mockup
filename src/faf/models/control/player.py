from faf.models.data.player import Player


class ModelPlayerUpdater:
    def __init__(self, models, player_msg, chat_updater):
        self._models = models
        self._chat_updater = chat_updater
        player_msg.new.subscribe(self.add_player_from_msg)

    @property
    def _players(self):
        return self._models.players

    @property
    def _games(self):
        return self._models.games

    @property
    def _current_player_game(self):
        return self._models.current_player_game

    def add_player_from_msg(self, msg):
        self.add_or_update_player(msg["login"], msg)
        return self._players[msg["login"]]

    def add_or_update_player(self, pid, attrs):
        if pid not in self._games:
            self._add_player(pid, attrs)
        else:
            self._update_player(pid, attrs)

    def _add_player(self, pid, attrs):
        player = Player(self._current_player_game, pid)
        player.update(attrs)
        self._players.add(player)
        self._players.added.on_next(player)
        player_game = self._current_player_game.get(pid)
        if player_game is not None:
            player_game._player_came_online()

        # This can emit events later, since game/player have no connection to
        # chatters
        self._chat_updater.on_player_added(player)

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

        self._chat_updater.on_player_removed(player)
