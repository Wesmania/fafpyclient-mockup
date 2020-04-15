import sys
import os

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from lobbyserver.server import LobbyServer


def get_app():
    sys.argv += ["--style", "Material"]
    return QGuiApplication(sys.argv)


if __name__ == "__main__":
    app = get_app()

    lobby_server = LobbyServer.build("lobby.faforever.com", 8001)

    root_path = os.path.join(os.path.dirname(__file__), "..")
    qml_file = os.path.join(root_path, "res/ui/main_window/ToplevelWindow.qml")

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("ROOT_PATH", root_path)
    ctx.setContextProperty("loginController", lobby_server.login)
    engine.load(qml_file)

    sys.exit(app.exec_())
