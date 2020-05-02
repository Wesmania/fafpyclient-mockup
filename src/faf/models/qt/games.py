from PySide2.QtCore import Qt

from faf.qt import InternalModelQtProxy, QtRoleEnum


class GameRoles(QtRoleEnum):
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
    def __init__(self, games):
        InternalModelQtProxy.__init__(self, games)
        for role in GameRoles:
            self._update_roles_at(lambda g: getattr(g, f"obs_{role.name}"),
                                  role)

    def roleNames(self):
        return GameRoles.role_names()

    def role(self, game, role):
        if role < Qt.UserRole or role >= len(GameRoles) + Qt.UserRole:
            return None
        role = GameRoles(role)
        return getattr(game, role.name)
