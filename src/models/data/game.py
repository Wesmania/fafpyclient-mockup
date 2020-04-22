from enum import Enum
from models.base.item import ModelItem


class GameState(Enum):
    OPEN = "open"
    PLAYING = "playing"
    CLOSED = "closed"


# This enum has a counterpart on the server
class GameVisibility(Enum):
    PUBLIC = "public"
    FRIENDS = "friends"


class Game(ModelItem):
    def __init__(self, id_):
        ModelItem.__init__(self)

        self.id = id_

        self._add_obs("state", GameState.OPEN)
        self._add_obs("launched_at", 0)
        self._add_obs("num_players", 0)
        self._add_obs("max_players", 0)
        self._add_obs("title", "")
        self._add_obs("host", "")
        self._add_obs("mapname", "")
        self._add_obs("map_file_path", "")
        self._add_obs("teams", {})
        self._add_obs("featured_mod", "")
        self._add_obs("sim_mods", [])
        self._add_obs("password_protected", False)
        self._add_obs("visibility", GameVisibility.PUBLIC)

    @property
    def id_key(self):
        return self.id

    @property
    def players(self):
        if self.teams is None:
            return set()
        return set(name for team in self.teams.values() for name in team)
