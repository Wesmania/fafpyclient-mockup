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


class Relation:
    def __init__(self, first_name, second_name):
        self._first_name = first_name
        self._second_name = second_name
        self._by_first = {}
        self._by_second = {}

    def by_first(self, idx):
        return self._by_first.get(idx)

    def by_second(self, idx):
        return self._by_second.get(idx)

    def by(self, name, idx):
        if name == self._first_name:
            return self.by_first(idx)
        elif name == self._second_name:
            return self.by_second(idx)
        else:
            raise ValueError


class SingleRelation(Relation):
    # Returns two lists indicating which items changed.
    def add(self, first, second):
        old_second = self._by_first.get(first)
        old_first = self._by_second.get(second)
        if second is old_second:
            return ([], [])

        self._by_first[first] = second
        self._by_second[second] = first
        if old_second is not None:
            del self._by_first[old_first]
            del self._by_second[old_second]

        firsts = [e for e in [first, old_first] if e is not None]
        seconds = [e for e in [second, old_second] if e is not None]
        return (firsts, seconds)

    def remove(self, first, second):
        if self._by_first.get(first) is None:
            return ([], [])
        del self._by_first[first]
        del self._by_second[second]
        return ([first], [second])
