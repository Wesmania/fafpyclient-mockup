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


class Channel(ModelItem):
    def __init__(self, id_):
        ModelItem.__init__(self)
        self.id = id_

        self._add_obs("topic", "")
        self.lines = []
        self.line_added = Subject()
        self.lines_removed = Subject()
        self.chatters = ModelSet()

    @property
    def id_key(self):
        return self.id

    def complete(self):
        ModelItem.complete(self)
        self.line_added.on_completed()
        self.lines_removed.on_completed()
        self.chatters.complete()
