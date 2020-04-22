from enum import Enum
import rx
from rx import operators as ops
from PySide2.QtCore import Qt

from qt.model import QtListModel


class GameRoles(Enum):
    title = 0
    mod = 1
    players = 2
    avg_rating = 3
    host = 4


class GameListQtModel(QtListModel):
    def __init__(self, games):
        QtListModel.__init__(self)
        self._games = games
        games.added.subscribe(self._add_game)
        games.removed.subscribe(self._remove_game)
        games.cleared.subscribe(self._clear_games)

        self._update_roles_at(lambda g: g.obs_title, [GameRoles.title])
        self._update_roles_at(lambda g: g.obs_featured_mod, [GameRoles.mod])
        self._update_roles_at(
            lambda g: rx.merge(
                g.obs_num_players,
                g.obs_max_players),
            [GameRoles.players])
        self._update_roles_at(lambda g: g.obs_host, [GameRoles.host])

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

        if role is GameRoles.title:
            return game.title
        if role is GameRoles.mod:
            return game.featured_mod
        if role is GameRoles.players:
            return f"{game.num_players}/{game.max_players}"
        if role is GameRoles.avg_rating:
            return 1000     # TODO
        if role is GameRoles.host:
            return game.host

    def _update_stream(self, stream_selector):
        def select(game):
            return stream_selector(game).pipe(ops.map(lambda _: game))

        return self._games.added.pipe(
            ops.map(select),
            ops.merge_all()
        )

    def _update_roles_at(self, stream_selector, roles):
        role_values = [r.value for r in roles]
        self._update_stream(stream_selector).subscribe(
            lambda g: self._update(g, role_values))
