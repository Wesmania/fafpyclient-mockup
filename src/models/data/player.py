from rx.subject import Subject
from models.base.item import ModelItem


class Player(ModelItem):
    def __init__(self, current_player_game, login):
        ModelItem.__init__(self)
        self._current_player_game = current_player_game

        self.login = login
        self._add_obs("id", 0)
        self._add_obs("global_rating", (1500, 500))
        self._add_obs("ladder_rating", (1500, 500))
        self._add_obs("number_of_games", 0)
        self._add_obs("avatar")
        self._add_obs("country")
        self._add_obs("clan")
        self._add_obs("league")

        self.obs_game = Subject()

    # The game this player is currently playing.
    @property
    def game(self):
        return self._current_player_game.get(self.id_key)

    def complete(self):
        ModelItem.complete(self)
        self.obs_game.on_completed()

    # Unfortunately, games refer to players by login.
    # I have no idea how this plays with renaming, hopefully the server doesn't
    # change player names mid-session
    @property
    def id_key(self):
        return self.login
