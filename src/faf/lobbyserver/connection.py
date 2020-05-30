from enum import Enum
from rx.subject import Subject, BehaviorSubject
from rx import operators as ops
from PySide2 import QtCore, QtNetwork


class ConnectionState(Enum):
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2


class LobbyConnection:
    """
    GUARANTEES:
    - After calling connect, connection will leave disconnected state.
    """

    def __init__(self, host, port):
        self.socket = QtNetwork.QTcpSocket()
        self.socket.stateChanged.connect(self._on_socket_state_change)
        self.socket.readyRead.connect(self.read)
        self.socket.error.connect(self._on_error)
        self.socket.setSocketOption(QtNetwork.QTcpSocket.KeepAliveOption, 1)

        self._host = host
        self._port = port
        self.block_size = 0

        self._obs_state = BehaviorSubject(ConnectionState.DISCONNECTED)
        self.obs_state = self._obs_state.pipe(
            ops.distinct_until_changed()
        )
        self.message_stream = Subject()

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
        return self._obs_state.value

    def _on_socket_state_change(self, state):
        s = self._socket_state(state)
        if s is ConnectionState.DISCONNECTED:
            self.block_size = 0
        self._obs_state.on_next(s)

    # Conflict with PySide2 signals!
    # Idempotent
    def connect_(self):
        if self.state is not ConnectionState.DISCONNECTED:
            return
        self.socket.connectToHost(self._host, self._port)

    def disconnect_(self):
        self.socket.disconnectFromHost()

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
            self.block_size = 0
            self.message_stream.on_next(data)

    def write(self, data):
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.ReadWrite)
        out.setVersion(QtCore.QDataStream.Qt_4_2)
        out.writeUInt32(2 * len(data) + 4)
        out.writeQString(data)
        if self.socket.state() == QtNetwork.QAbstractSocket.ConnectedState:
            self.socket.write(block)

    def _on_error(self):
        self.disconnect_()
