from PySide2.QtCore import Qt

from faf.qt import InternalModelQtProxy, QtRoleEnum
from faf.resources.images import ImageCache


class GameRoles(QtRoleEnum):
    # TODO - for some absurd reason, putting map_preview on the very end causes
    # only one message to get parsed, and for others to be lost. WTF!?!?!?
    map_preview = ()

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


class GamesQtModel(InternalModelQtProxy):
    def __init__(self, games, map_previews: ImageCache):
        InternalModelQtProxy.__init__(self, games)
        self._map_previews = map_previews
        map_previews.image_available.connect(self._on_map_preview_available)

        for role in GameRoles:
            if role is GameRoles.map_preview:
                continue
            self._update_roles_at(lambda g: getattr(g, f"obs_{role.name}"),
                                  role)

    def roleNames(self):
        return GameRoles.role_names()

    def role(self, game, role):
        if role < Qt.UserRole or role >= len(GameRoles) + Qt.UserRole:
            return None
        role = GameRoles(role)
        if role is GameRoles.map_preview:
            return self._map_preview(game)
        return getattr(game, role.name)

    def _map_preview_name(self, game):
        return game.mapname.lower()

    def _on_map_preview_available(self, mapname):
        for idx, game in enumerate(self._items.values()):
            if self._map_preview_name(game) == mapname:
                self._update(game.id_key, [GameRoles.map_preview.value])

    def _map_preview(self, game):
        name = self._map_preview_name(game)
        return self._map_previews.get(name)
