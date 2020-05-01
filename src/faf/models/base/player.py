from collections.abc import Mapping
from faf.models.data.game import GameState


class PlayerCurrentGameRelation(Mapping):
    def __init__(self):
        Mapping.__init__(self)
        self._items = {}

    def __getitem__(self, key):
        return self._items[key]

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def _player_did_change_game(self, new, old):
        # Removing or setting new game should always happen
        if new is None or old is None:
            return True
        if new.id_key == old.id_key:
            return False

        # Games should be not closed now
        # Lobbies always take precedence - if there are 2 at once, tough luck
        if new.state == GameState.OPEN:
            return True
        if old.state == GameState.OPEN:
            return False

        # Both games have started, pick later one
        if new.launched_at is None:
            return False
        if old.launched_at is None:
            return True
        return new.launched_at > old.launched_at

    def add_game_to_player(self, pid, game):
        old_game = self.get(pid)
        if not self._player_did_change_game(game, old_game):
            return False
        self._items[pid] = game
        return True

    def remove_game_from_player(self, pid, game):
        old_game = self.get(pid)
        if old_game is None or old_game.id_key != game.id_key:
            return False
        del self._items[pid]
        return True

    def add_players(self, pids, game):
        changed_pids = []
        for pid in game.players:
            if self.add_game_to_player(pid, game):
                changed_pids.append(pid)
        return changed_pids

    def remove_players(self, pids, game):
        changed_pids = []
        for pid in game.players:
            if self.remove_game_from_player(pid, game):
                changed_pids.append(pid)
        return changed_pids

    def clear(self):
        self._items.clear()
