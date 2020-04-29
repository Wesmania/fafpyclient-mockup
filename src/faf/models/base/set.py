from rx.subject import Subject


class ModelSet:
    def __init__(self):
        self._items = {}
        self.added = Subject()
        self.removed = Subject()
        self.cleared = Subject()

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, key):
        return key in self._items

    def get(self, key, default=None):
        return self._items.get(key, default)

    def add(self, item):
        self._items[item.id_key] = item

    def remove(self, item):
        del self._items[item.id_key]

    def clear(self):
        self._items.clear()

    def complete(self):
        self.added.on_completed()
        self.removed.on_completed()
        self.cleared.on_completed()
