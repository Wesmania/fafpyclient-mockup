from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt


class QListModel(QAbstractListModel):
    def __init__(self):
        QAbstractListModel.__init__(self)
        self.items = []

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        return len(self.items)

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return None
        if not index.isValid() or index.row() >= len(self.items):
            return None
        return self.items[index.row()]

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self.items) - 1)
        self.items = []
        self.endRemoveRows()

    def set(self, items):
        self.clear()
        self.beginInsertRows(QModelIndex(), 0, len(items) - 1)
        self.items = items
        self.endInsertRows()
