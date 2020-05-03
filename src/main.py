import sys
import os
import asyncio
from asyncqt import QEventLoop

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWebEngine import QtWebEngine

from faf.lobbyserver import LobbyServer
from faf.session import LoginSession
from faf.tabs.news import NewsTab
from faf.tabs.games import GamesTab
from faf.tabs.chat import ChatTab
from faf.models import Models
from faf.irc import Irc


def get_app():
    sys.argv += ["--style", "Material"]
    QtWebEngine.initialize()
    return QGuiApplication(sys.argv)


def set_loop(app):
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)


if __name__ == "__main__":
    app = get_app()
    set_loop(app)

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()

    lobby_server = LobbyServer("lobby.faforever.com", 8001)
    irc = Irc('irc.faforever.com', 6667)
    models = Models(lobby_server, irc)

    login_session = LoginSession(lobby_server, irc, models, ctx)
    news = NewsTab(login_session, ctx)
    games = GamesTab(models, ctx)
    chat = ChatTab(models, ctx)

    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    qml_file = os.path.join(root_path, "res/ui/main_window/ToplevelWindow.qml")

    ctx.setContextProperty("ROOT_PATH", root_path)
    engine.load(qml_file)

    loop = asyncio.get_event_loop()
    with loop:
        sys.exit(loop.run_forever())
