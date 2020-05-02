from enum import Enum
from PySide2.QtCore import Qt


class QtRoleEnum(Enum):
    def __new__(cls):
        value = len(cls.__members__) + Qt.UserRole
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    @classmethod
    def role_names(cls):
        return {
            role.value: role.name.encode() for role in cls
        }
