from PySide2.QtCore import Qt, QSortFilterProxyModel

from faf.qt import InternalModelQtProxy, QtRoleEnum


class ChatterRoles(QtRoleEnum):
    nick = ()
    is_op = ()


class ChattersQtModel(InternalModelQtProxy):
    def __init__(self, chatters):
        InternalModelQtProxy.__init__(self, chatters)
        self._update_roles_at(lambda c: c.obs_mode,
                              ChatterRoles.is_op)

    def roleNames(self):
        return ChatterRoles.role_names()

    def role(self, chatter, role):
        if role < Qt.UserRole or role >= len(ChatterRoles) + Qt.UserRole:
            return None
        role = ChatterRoles(role)
        if role is ChatterRoles.nick:
            return chatter.nick
        if role is ChatterRoles.is_op:
            return chatter.is_op


class ChattersQtFilterModel(QSortFilterProxyModel):
    def __init__(self, chatter_model):
        QSortFilterProxyModel.__init__(self)
        self.setSourceModel(chatter_model)
        self.sort(0)

    def lessThan(self, left_index, right_index):
        source = self.sourceModel()
        left = source.from_index(left_index)
        right = source.from_index(right_index)
        return left.nick.lower() < right.nick.lower()
