from models.base.set import ModelSet
from models.base.player import PlayerCurrentGameRelation

from models.control.game import ModelGameUpdater
from models.control.player import ModelPlayerUpdater
from models.control.login import ModelLoginUpdater


class ModelData:
    """
    Represents various sets of data with relations - games, players, chatters
    etc. We need to keep track of those to present game and chat user lists,
    and to check status of games, players and such.

    We take extra care to keep these models consistent - we never emit change
    events halfway through updating models.
    """
    def __init__(self):
        self.games = ModelSet()
        self.players = ModelSet()
        self.current_player_game = PlayerCurrentGameRelation()


class ModelControl:
    def __init__(self, data, lobby_server):
        self.game_updater = ModelGameUpdater(data, lobby_server.game_msg)
        self.player_updater = ModelPlayerUpdater(data, lobby_server.player_msg)
        self.login_updater = ModelLoginUpdater(data, lobby_server.login)


class Models:
    def __init__(self, lobby_server):
        self.data = ModelData()
        self.control = ModelControl(self.data, lobby_server)
