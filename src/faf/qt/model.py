from PySide2.QtCore import QAbstractListModel, QModelIndex
from sortedcontainers import SortedDict


# QtListModel with a dict underneath.
class QtDictListModel(QAbstractListModel):
    def __init__(self):
        QAbstractListModel.__init__(self)
        self._items = SortedDict()

    def role(self, item, role):
        return item

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        return len(self._items)

    def from_index(self, index):
        if not index.isValid() or index.row() >= len(self._items):
            return None
        return self._items.peekitem(index.row())[1]

    def data(self, index, role):
        item = self.from_index(index)
        if item is None:
            return None
        return self.role(item, role)

    def _add(self, key, item):
        assert key not in self._items
        next_index = self._items.bisect_left(key)
        self.beginInsertRows(QModelIndex(), next_index, next_index)
        self._items[key] = item
        self.endInsertRows()

    # TODO - removal is O(n).
    def _remove(self, key):
        assert key in self._items
        item = self._items[key]
        item_index = self._items.index(key)
        self.beginRemoveRows(QModelIndex(), item_index, item_index)
        del self._items[key]
        self.endRemoveRows()

    def _clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._items) - 1)
        self._items.clear()
        self.endRemoveRows()

    # O(n). Rework if it's too slow.
    def _update(self, key, roles=None):
        item_index = self._items.index(key)
        index = self.index(item_index, 0)
        if roles is None:
            self.dataChanged.emit(index, index)
        else:
            self.dataChanged.emit(index, index, roles)


# QtListModel with a list underneath.
class QtPlainListModel(QAbstractListModel):
    def __init__(self):
        QAbstractListModel.__init__(self)
        self._itemlist = []

    def role(self, item, role):
        return item

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        return len(self._itemlist)

    def from_index(self, index):
        if not index.isValid() or index.row() >= len(self._itemlist):
            return None
        return self._itemlist[index.row()]

    def data(self, index, role):
        item = self.from_index(index)
        if item is None:
            return None
        return self.role(item, role)

    def _append(self, item):
        next_index = len(self._itemlist)
        self.beginInsertRows(QModelIndex(), next_index, next_index)
        self._itemlist.append(item)
        self.endInsertRows()

    # Removes from start to end, not inclusive.
    def _remove_range(self, start, end):
        self.beginRemoveRows(QModelIndex(), start, end - 1)
        del self._itemlist[start:end]
        self.endRemoveRows()

    def _clear(self):
        self._remove_range(0, len(self._itemlist))

    def _set_list(self, items):
        self._clear()
        self.beginInsertRows(QModelIndex(), 0, len(items) - 1)
        self._itemlist = items
        self.endInsertRows()

    def _item_index(self, item):
        return self._itemlist.index(item)

    def _update(self, index, roles=None):
        index = self.index(index, 0)
        if roles is None:
            self.dataChanged.emit(index, index)
        else:
            self.dataChanged.emit(index, index, roles)
