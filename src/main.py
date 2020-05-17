import sys
import os
import asyncio
import aiohttp
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
from faf.resources import Resources
from faf.qt_models import QtModels
from faf.irc import Irc


def get_app():
    sys.argv += ["--style", "Material"]
    QtWebEngine.initialize()
    return QGuiApplication(sys.argv)


def set_loop(app):
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)


def get_resources(http_session):
    config = {
        'map_previews': {
            'cache_dir': os.path.realpath('../cache/map_previews/{name}.png'),
            'access_url': 'https://content.faforever.com/faf/vault/map_previews/small/{name}.png',
            'default_image': os.path.realpath('../res/icons/games/unknown_map.png'),
        }
    }
    return Resources(config, http_session)


if __name__ == "__main__":
    app = get_app()
    set_loop(app)
    loop = asyncio.get_event_loop()

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()

    http_session = aiohttp.ClientSession(loop=loop)
    lobby_server = LobbyServer("lobby.faforever.com", 8001)
    irc = Irc('irc.faforever.com', 6667)
    resources = get_resources(http_session)

    models = Models(lobby_server, irc)

    login_session = LoginSession(lobby_server, irc, models, ctx)
    qt_models = QtModels(models, resources)

    news = NewsTab(login_session, ctx)
    games = GamesTab(qt_models, ctx)
    chat = ChatTab(irc, models, ctx)

    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    qml_file = os.path.join(root_path, "res/ui/main_window/ToplevelWindow.qml")

    ctx.setContextProperty("ROOT_PATH", root_path)
    engine.load(qml_file)

    with loop:
        sys.exit(loop.run_forever())
