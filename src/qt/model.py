from PySide2.QtCore import QAbstractListModel, QModelIndex


class QtListModel(QAbstractListModel):
    def __init__(self):
        QAbstractListModel.__init__(self)
        self._items = {}
        self._itemlist = []  # For queries

    def role(self, item, role):
        return item

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        return len(self._itemlist)

    def data(self, index, role):
        if not index.isValid() or index.row() >= len(self._itemlist):
            return None
        item = self._itemlist[index.row()]
        return self.role(item, role)

    def _add(self, key, item):
        assert key not in self._items
        next_index = len(self._itemlist)
        self.beginInsertRows(QModelIndex(), next_index, next_index)
        self._items[key] = item
        self._itemlist.append(item)
        self.endInsertRows()

    # TODO - removal is O(n).
    def _remove(self, key):
        assert key in self._items
        item = self._items[key]
        item_index = self._itemlist.index(item)
        self.beginRemoveRows(QModelIndex(), item_index, item_index)
        del self._items[key]
        self._itemlist.pop(item_index)
        self.endRemoveRows()

    def _clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._items) - 1)
        self._items.clear()
        self._itemlist.clear()
        self.endRemoveRows()

    def _set_list(self, items):
        self._clear()
        self.beginInsertRows(QModelIndex(), 0, len(items) - 1)
        self._items = {i: e for i, e in enumerate(items)}
        self._itemlist = items
        self.endInsertRows()

    # O(n). Rework if it's too slow.
    def _update(self, item, roles=None):
        item_index = self._itemlist.index(item)
        index = self.index(item_index, 0)
        if roles is None:
            self.dataChanged.emit(index, index)
        else:
            self.dataChanged.emit(index, index, roles)
