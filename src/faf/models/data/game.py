from enum import Enum
import rx
from rx import operators as ops
from rx.subject import Subject
from faf.models.base import ModelItem


class GameState(Enum):
    OPEN = "open"
    PLAYING = "playing"
    CLOSED = "closed"


# This enum has a counterpart on the server
class GameVisibility(Enum):
    PUBLIC = "public"
    FRIENDS = "friends"


class Game(ModelItem):
    def __init__(self, id_, player_set):
        ModelItem.__init__(self)

        self._player_set = player_set
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

        # Workaround for game info being sent before player info.
        self._obs_player_came_online = Subject()
        self.obs_teams = self._repeat_when_player_comes_online(self.obs_teams)
        self.obs_host = self._repeat_when_player_comes_online(self.obs_host)

        # Misses (rare) cases when a player's rating changes. Not a problem.
        self.obs_average_rating = self.obs_teams.pipe(
            ops.map(lambda _: self.average_rating())
        )

    def _player_came_online(self):
        self._obs_player_came_online.on_next(None)

    def _repeat_when_player_comes_online(self, obs):
        return rx.combine_latest(
            self.obs_teams, self._obs_player_came_online).pipe(
                ops.map(lambda t: t[0])
            )

    @property
    def average_rating(self):
        player_ids = self.players
        players = [self._player_set[p] for p in player_ids
                   if p in self._player_set]
        if not players:
            return 0
        return sum([p.rating_estimate for p in players]) // len(players)

    @property
    def id_key(self):
        return self.id

    @property
    def players(self):
        if self.teams is None:
            return set()
        return set(name for team in self.teams.values() for name in team)
