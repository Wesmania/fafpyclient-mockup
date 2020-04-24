from enum import Enum
from rx import operators as ops
from PySide2.QtCore import Qt

from qt.model import QtListModel


class GameRoles(Enum):
    title = 0
    featured_mod = 1
    num_players = 2
    max_players = 3
    average_rating = 4
    host = 5


class GameListQtModel(QtListModel):
    def __init__(self, games):
        QtListModel.__init__(self)
        self._games = games

        games.added.subscribe(self._add_game)
        games.removed.subscribe(self._remove_game)
        games.cleared.subscribe(self._clear_games)

        for role in GameRoles:
            self._update_roles_at(lambda g: getattr(g, f"obs_{role.name}"),
                                  role)

    def _add_game(self, game):
        self._add(game.id_key, game)

    def _remove_game(self, game):
        self._remove(game.id_key)

    def _clear_games(self, _):
        self._clear()

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        return len(self._items)

    def roleNames(self):
        return {
            role.value + Qt.UserRole: role.name.encode()
            for role in GameRoles
        }

    def role(self, game, role):
        rnum = role - Qt.UserRole
        if rnum < 0 or rnum >= len(GameRoles):
            return None
        role = GameRoles(rnum)
        return getattr(game, role.name)

    def _update_stream(self, stream_selector):

        def select(game):
            return stream_selector(game).pipe(
                ops.map(lambda _: game)
            )

        return self._games.added.pipe(
            ops.map(select),
            ops.merge_all()
        )

    def _update_roles_at(self, stream_selector, role):
        self._update_stream(stream_selector).subscribe(
            lambda g: self._update(g, role.value))
