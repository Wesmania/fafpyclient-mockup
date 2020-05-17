from faf.models.base import ModelSet
from faf.models.base.player import PlayerCurrentGameRelation
from faf.models.control import ModelGameUpdater, ModelPlayerUpdater, \
    ModelChatUpdater


class ModelData:
    """
    Represents various sets of data with relations - games, players, chatters
    etc. We need to keep track of those to present game and chat user lists,
    and to check status of games, players and such.
    """
    def __init__(self):
        self.games = ModelSet()
        self.players = ModelSet()
        self.current_player_game = PlayerCurrentGameRelation()
        self.chat = ModelSet()


class ModelControl:
    def __init__(self, data, lobby_server, irc):
        self.chat_updater = ModelChatUpdater(data, irc.client)
        self.game_updater = ModelGameUpdater(data, lobby_server.game_msg)
        self.player_updater = ModelPlayerUpdater(data, lobby_server.player_msg,
                                                 self.chat_updater)


class Models:
    def __init__(self, lobby_server, irc):
        self.data = ModelData()
        self.control = ModelControl(self.data, lobby_server, irc)
