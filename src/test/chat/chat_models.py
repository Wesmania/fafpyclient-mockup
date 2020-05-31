from faf.models.base import ModelSet
from faf.models.base.player import PlayerCurrentGameRelation
from faf.models.control import ModelChatUpdater


class ModelData:
    def __init__(self):
        self.games = ModelSet()
        self.players = ModelSet()
        self.current_player_game = PlayerCurrentGameRelation()
        self.chat = ModelSet()


class ModelControl:
    def __init__(self, data, irc):
        self.chat_updater = ModelChatUpdater(data, irc.client)


class QtModels:
    def __init__(self, model_data):
        pass


class Models:
    def __init__(self, irc):
        self.data = ModelData()
        self.control = ModelControl(self.data, irc)
        self.qt = QtModels(self.data)
