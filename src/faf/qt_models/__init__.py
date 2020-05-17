__all__ = ["GamesQtModel"]

from faf.qt_models.games import GamesQtModel


class QtModels:
    """
    Any qt models that are used in multiple places in the client go here.
    """
    def __init__(self, models, resources):
        self.games = GamesQtModel(models.data.games, resources.map_previews)
