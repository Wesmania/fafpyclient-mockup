from PySide2.QtCore import Qt

from faf.qt import QtPlainListModel, QtRoleEnum


class ChatLineRoles(QtRoleEnum):
    nick = ()
    message = ()


class ChatLineQtModel(QtPlainListModel):
    def __init__(self, chat_lines):
        QtPlainListModel.__init__(self)
        self._lines = chat_lines
        self._lines.added.subscribe(self._add_line)
        self._lines.removed.subscribe(self._remove_lines)

    def _add_line(self, line):
        self._append(line)

    def _remove_lines(self, count):
        self._remove_range(0, count)

    def roleNames(self):
        return ChatLineRoles.role_names()

    def role(self, chat_line, role):
        if role < Qt.UserRole or role >= len(ChatLineRoles) + Qt.UserRole:
            return None
        role = ChatLineRoles(role)
        if role is ChatLineRoles.nick:
            return chat_line.nick
        if role is ChatLineRoles.message:
            return chat_line.message
