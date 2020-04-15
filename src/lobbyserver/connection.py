from PySide2 import QtCore, QtNetwork
from enum import IntEnum


class ConnectionState(IntEnum):
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2


def foo(bar):
    pass


class LobbyConnection(QtCore.QObject):
    """
    GUARANTEES:
    - After calling connect, connection will leave disconnected state.
    """
    connected = QtCore.Signal()
    disconnected = QtCore.Signal()
    new_message = QtCore.Signal(object)

    def __init__(self, host, port):
        QtCore.QObject.__init__(self)
        self.socket = QtNetwork.QTcpSocket()
        self.socket.stateChanged.connect(self._on_socket_state_change)
        self.socket.readyRead.connect(self.read)
        self.socket.error.connect(self._error)
        self.socket.setSocketOption(QtNetwork.QTcpSocket.KeepAliveOption, 1)

        self._host = host
        self._port = port
        self._state = ConnectionState.DISCONNECTED
        self.block_size = 0

    def _socket_state(self, s):
        qas = QtNetwork.QAbstractSocket
        if s in [qas.ConnectedState, qas.ClosingState]:
            return ConnectionState.CONNECTED
        elif s in [qas.BoundState, qas.HostLookupState,
                   qas.ConnectingState]:
            return ConnectionState.CONNECTING
        else:
            return ConnectionState.DISCONNECTED

    @property
    def state(self):
        return self._state

    def _on_socket_state_change(self, state):
        new = self._socket_state(state)
        old, self._state = self._state, new
        if new is old:
            return

        if new is ConnectionState.DISCONNECTED:
            self.disconnected.emit()
        elif new is ConnectionState.CONNECTED:
            self.connected.emit()

    # Conflict with PySide2 signals!
    def connect_(self):
        if self.state is not ConnectionState.DISCONNECTED:
            return
        self.socket.connectToHost(self._host, self._port)

    def disconnect_(self):
        self.socket.disconnectFromHost()

    def _on_connected(self):
        self.connected.emit()

    def _on_disconnected(self):
        self.block_size = 0
        self.state = ConnectionState.DISCONNECTED

    def read(self):
        ins = QtCore.QDataStream(self.socket)
        ins.setVersion(QtCore.QDataStream.Qt_4_2)

        while not ins.atEnd():
            if self.block_size == 0:
                if self.socket.bytesAvailable() < 4:
                    return
                self.block_size = ins.readUInt32()
            if self.socket.bytesAvailable() < self.block_size:
                return

            data = ins.readQString()
            self.new_message.emit(data)
            self.block_size = 0

    def write(self, data):
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.ReadWrite)
        out.setVersion(QtCore.QDataStream.Qt_4_2)
        out.writeUInt32(2 * len(data) + 4)
        out.writeQString(data)
        self.socket.write(block)

    def _error(self, error):
        pass    # TODO
