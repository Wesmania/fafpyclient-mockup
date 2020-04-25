from enum import Enum
from rx import operators as ops
from PySide2.QtCore import Qt

from faf.qt import QtListModel


class GameRoles(Enum):
    def __new__(cls):
        value = len(cls.__members__) + Qt.UserRole
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    state = ()
    launched_at = ()
    num_players = ()
    max_players = ()
    title = ()
    host = ()
    mapname = ()
    map_file_path = ()
    teams = ()
    featured_mod = ()
    sim_mods = ()
    password_protected = ()
    visibility = ()
    average_rating = ()


class GamesQtModel(QtListModel):
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
            role.value: role.name.encode() for role in GameRoles
        }

    def role(self, game, role):
        if role < Qt.UserRole or role >= len(GameRoles) + Qt.UserRole:
            return None
        role = GameRoles(role)
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
