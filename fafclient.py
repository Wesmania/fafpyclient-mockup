import sys
import os

from PySide2.QtCore import QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtQml import QQmlApplicationEngine


if __name__ == "__main__":
    sys.argv += ["--style", "Material"]
    app = QGuiApplication(sys.argv)

    root_path = os.path.dirname(__file__)	# FIXME for pyinstaller and such
    qml_file = os.path.join(root_path, "res/ui/main_window/ToplevelWindow.qml")
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("ROOT_PATH", root_path)
    engine.load(qml_file)
    sys.exit(app.exec_())
