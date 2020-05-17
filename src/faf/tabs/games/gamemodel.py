from enum import Enum
from PySide2.QtCore import QSortFilterProxyModel, Signal, Slot, Property

from faf.models.data.game import GameState, GameVisibility


# TODO - ascending / descending sort
class GameSortOptions(Enum):
    AGE = 0
    NUM_PLAYERS = 1
    MAX_PLAYERS = 2
    AVG_RATING = 3
    TITLE = 4


class LobbyGamesModel(QSortFilterProxyModel):
    on_priv_games_visible = Signal(bool)
    on_modded_games_visible = Signal(bool)

    def __init__(self, game_model):
        QSortFilterProxyModel.__init__(self)
        self._game_model = game_model

        self._modded_games_visible = False
        self._private_games_visible = False
        self._sort_by = GameSortOptions.AGE
        self.setSourceModel(game_model)
        self.sort(0)

    def _from_index(self, index):
        return self._game_model.from_index(index)

    def filterAcceptsRow(self, row, parent):
        index = self.sourceModel().index(row, 0, parent)
        game = self.sourceModel().from_index(index)
        if game is None:
            return False
        if game.state is not GameState.OPEN:
            return False
        if not self._modded_games_visible:
            if game.featured_mod != "faf":
                return False
        if not self._private_games_visible:
            if game.visibility is GameVisibility.FRIENDS:
                return False
        return True

    def _lt_by_role(self, left, right):
        if self._sort_by is GameSortOptions.AGE:
            return left.id < right.id
        elif self._sort_by is GameSortOptions.NUM_PLAYERS:
            return left.num_players < right.num_players
        elif self._sort_by is GameSortOptions.MAX_PLAYERS:
            return left.max_players < right.max_players
        elif self._sort_by is GameSortOptions.AVG_RATING:
            return left.average_rating < right.average_rating
        elif self._sort_by is GameSortOptions.TITLE:
            return left.title.lower() < right.title.lower()

    def lessThan(self, left, right):
        left = self._from_index(left)
        right = self._from_index(right)

        if self._lt_by_role(left, right):
            return True
        elif self._lt_by_role(right, left):
            return False
        return left.id < right.id

    @Slot(int)
    def set_sort_type(self, type_num):
        self._sort_by = GameSortOptions(type_num)
        self.invalidate()

    def set_priv_games_visible(self, v):
        self._private_games_visible = v
        self.invalidate()
        self.on_priv_games_visible.emit(v)

    def get_priv_games_visible(self):
        return self._private_games_visible

    def set_modded_games_visible(self, v):
        self._modded_games_visible = v
        self.invalidate()
        self.on_modded_games_visible.emit(v)

    def get_modded_games_visible(self):
        return self._modded_games_visible

    private_games_visible = Property(bool, get_priv_games_visible,
                                     set_priv_games_visible,
                                     notify=on_priv_games_visible)
    modded_games_visible = Property(bool, get_modded_games_visible,
                                    set_modded_games_visible,
                                    notify=on_modded_games_visible)
