from faf.tabs.games.gamemodel import LobbyGamesModel


class GamesTab:
    def __init__(self, qt_models, qml_context):
        self.lobby_game_model = LobbyGamesModel(qt_models.games)
        qml_context.setContextProperty("faf__tabs__games__model",
                                       self.lobby_game_model)
