from PySide2.QtCore import QObject, Signal, QTimer

from faf.irc.irc import MessageType, IrcNickWithMode


class MockIrcClient(QObject):
    at_connected = Signal()
    at_disconnected = Signal()
    at_nickserv_identified = Signal()
    at_names = Signal(str, list)
    at_join = Signal(str, IrcNickWithMode)
    at_part = Signal(str, IrcNickWithMode, str)
    at_quit = Signal(IrcNickWithMode, str)
    at_topic = Signal(str, str)
    at_usermode = Signal(IrcNickWithMode, str)
    at_rename = Signal(IrcNickWithMode, IrcNickWithMode)
    at_message = Signal(IrcNickWithMode, str, str, MessageType)

    def __init__(self):
        QObject.__init__(self)

    def send_privmsg(self, target, message):
        pass

    def send_action(self, target, message):
        pass

    def join(self, channel):
        pass

    def part(self, channel):
        pass

    def topic(self, channel, message):
        pass

    def connect_(self, username, password):
        QTimer.singleShot(0, self, self._do_connect)

    def _do_connect(self):
        self.at_connected.emit()
        self.at_nickserv_identified.emit()

    def disconnect_(self):
        QTimer.singleShot(0, self, self.at_disconnected.emit)
