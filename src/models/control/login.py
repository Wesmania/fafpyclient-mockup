class ModelLoginUpdater:
    def __init__(self, models, login):
        self._models = models
        self._login = login
        login.logged_out.connect(self._clear_models)

    def _clear_models(self):
        self._models.games.clear()
        self._models.players.clear()
        self._models.current_player_game.clear()

        self._models.games.cleared.on_next(None)
        self._models.players.cleared.on_next(None)
