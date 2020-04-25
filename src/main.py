import sys
import os

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWebEngine import QtWebEngine

from faf.lobbyserver import LobbyServer
from faf.news import News
from faf.models import Models
from faf.gametab.gamemodel import GameListQtModel


def get_app():
    sys.argv += ["--style", "Material"]
    QtWebEngine.initialize()
    return QGuiApplication(sys.argv)


if __name__ == "__main__":
    app = get_app()

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()

    lobby_server = LobbyServer("lobby.faforever.com", 8001, ctx)
    news = News.build(ctx)
    models = Models(lobby_server)
    qt_game_model = GameListQtModel(models.data.games)
    lobby_server.login.logged_in.connect(news.fetch)

    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    qml_file = os.path.join(root_path, "res/ui/main_window/ToplevelWindow.qml")

    ctx.setContextProperty("ROOT_PATH", root_path)
    ctx.setContextProperty("game_model", qt_game_model)
    engine.load(qml_file)

    sys.exit(app.exec_())
