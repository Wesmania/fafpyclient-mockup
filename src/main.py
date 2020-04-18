import sys
import os

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWebEngine import QtWebEngine

from lobbyserver.server import LobbyServer
from news.news import News


def get_app():
    sys.argv += ["--style", "Material"]
    QtWebEngine.initialize()
    return QGuiApplication(sys.argv)


if __name__ == "__main__":
    app = get_app()

    lobby_server = LobbyServer.build("lobby.faforever.com", 8001)
    news = News.build()
    lobby_server.login.logged_in.connect(news.fetch)

    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    qml_file = os.path.join(root_path, "res/ui/main_window/ToplevelWindow.qml")

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("ROOT_PATH", root_path)
    ctx.setContextProperty("loginController", lobby_server.login)
    ctx.setContextProperty("news", news)
    ctx.setContextProperty("news_model", news.model)
    engine.load(qml_file)

    sys.exit(app.exec_())
