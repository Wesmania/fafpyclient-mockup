from collections.abc import Mapping


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

    def add_game_to_player(self, pid, game):
        old_game = self.get(pid)
        if old_game is not None and old_game.id_key == game.id_key:
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
