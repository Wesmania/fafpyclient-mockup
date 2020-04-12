import sys
import os

from PySide2.QtCore import QUrl, Signal, Slot, QObject
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtQml import QQmlApplicationEngine


class LoginController(QObject):
    loginSignal = Signal(bool)

    def __init__(self):
        QObject.__init__(self)
        self._logged_in = False

    @property
    def logged_in(self):
        return self._logged_in

    @logged_in.setter
    def logged_in(self, val):
        signal = self._logged_in != val
        self._logged_in = val
        if signal:
            self.loginSignal.emit(self._logged_in)

    @Slot(str, str)
    def login(self, user, password):
        if user != "foo" or password != "bar":
            print(f"Invalid credentials: {foo}, {bar}")
        else:
            print("Logged in.")
            self.logged_in = True

    @Slot()
    def logout(self):
        self.logged_in = False
        print("Logged out.")


if __name__ == "__main__":
    sys.argv += ["--style", "Material"]
    app = QGuiApplication(sys.argv)

    login_c = LoginController()

    root_path = os.path.dirname(__file__)	# FIXME for pyinstaller and such
    qml_file = os.path.join(root_path, "res/ui/main_window/ToplevelWindow.qml")

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("ROOT_PATH", root_path)
    engine.rootContext().setContextProperty("loginController", login_c)
    engine.load(qml_file)

    sys.exit(app.exec_())
