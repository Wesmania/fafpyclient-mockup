from models.base.set import ModelSet
from models.base.player import PlayerCurrentGameRelation


class Models:
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
