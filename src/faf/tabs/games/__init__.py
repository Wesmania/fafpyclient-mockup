from faf.tabs.games.gamemodel import LobbyGamesModel


class GamesTab:
    def __init__(self, models, qml_context):
        self.lobby_game_model = LobbyGamesModel(models.qt.games)
        qml_context.setContextProperty("faf__tabs__games__model",
                                       self.lobby_game_model)
