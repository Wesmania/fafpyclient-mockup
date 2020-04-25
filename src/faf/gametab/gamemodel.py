from PySide2.QtCore import QSortFilterProxyModel

from faf.models.data.game import GameState
from faf.models.qt.games import GameRoles


class LobbyGamesModel(QSortFilterProxyModel):
    def __init__(self, game_model):
        QSortFilterProxyModel.__init__(self)
        self.setSourceModel(game_model)
        self.setSortRole(GameRoles.launched_at.value)
        # TODO - custom sorting via lessThan

    def filterAcceptsRow(self, row, parent):
        index = self.sourceModel().index(row, 0, parent)
        game = self.sourceModel().item_at(index)
        if game is None:
            return False
        return game.state is GameState.OPEN
