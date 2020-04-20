from collections.ABC import Mapping


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

    def set_player_game(self, pid, game):
        old_game = self.get(pid)
        if old_game is None and game is None:
            return False
        if (old_game, game) is not None and game is not None \
                and old_game.id_key == game.id_key:
            return False

        if game is not None:
            self[pid] = game
        else:
            del self[pid]
        return True
