from enum import Enum
from rx.subject import Subject
from faf.models.base import ModelItem, ModelSet


class ChannelType(Enum):
    PUBLIC = 1
    PRIVATE = 2


class ChannelID:
    def __init__(self, type_, name):
        self.type = type_
        self.name = name

    def __eq__(self, other):
        return self.type == other.type and self.name == other.name

    def __hash__(self):
        return hash((self.name, self.type))

    @classmethod
    def private(cls, name):
        return cls(ChannelType.PRIVATE, name)

    @classmethod
    def public(cls, name):
        return cls(ChannelType.PUBLIC, name)


class Lines:
    # TODO config
    MAX_LINES = 300
    REMOVE_BATCH = 50

    def __init__(self):
        self.lines = []
        self.added = Subject()
        self.removed = Subject()

    def __getitem__(self, n):
        return self.lines[n]

    def __iter__(self):
        return iter(self.lines)

    def __len__(self):
        return len(self.lines)

    def add(self, line):
        self.lines.append(line)
        self.added.on_next(line)
        self._check_trim()

    def clear(self):
        ll = len(self)
        self.lines.clear()
        self.removed.on_next(ll)

    def _check_trim(self):
        if len(self) > self.MAX_LINES:
            self.lines = self.lines[self.REMOVE_BATCH:]
            self.removed.on_next(self.REMOVE_BATCH)

    def complete(self):
        self.added.on_completed()
        self.removed.on_completed()


class Channel(ModelItem):
    def __init__(self, id_):
        ModelItem.__init__(self)
        self.id = id_

        self._add_obs("topic", "")
        self.lines = Lines()
        self.chatters = ModelSet()

    @property
    def id_key(self):
        return self.id

    def complete(self):
        ModelItem.complete(self)
        self.lines.complete()
        self.chatters.complete()
