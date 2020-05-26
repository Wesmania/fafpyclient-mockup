"""FAF client.

Usage:
  main.py --root <root_dir> -c <files>...

Options:
  -c <files>...   Configuration files to use. Last one is treated as user-writable config file.
  --root <root_dir> Root resource directory.
"""

import sys
import os
import asyncio
import aiohttp
from asyncqt import QSelectorEventLoop
from docopt import docopt

from PySide2.QtCore import QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWebEngine import QtWebEngine

from faf.config import Config
from faf.lobbyserver import LobbyServer
from faf.session import LoginSession
from faf.tabs.news import NewsTab
from faf.tabs.games import GamesTab
from faf.tabs.chat import ChatTab
from faf.models import Models
from faf.resources import Resources
from faf.qt_models import QtModels
from faf.irc import Irc
from faf.environ import Environment
from faf.tools import Tools


def get_app():
    args = [sys.argv[0], "--style", "Material"]
    QtWebEngine.initialize()
    return QGuiApplication(args)


def set_loop(app):
    # Asyncqt and kin are broken with the proactor loop on Windows
    loop = QSelectorEventLoop(app)
    asyncio.set_event_loop(loop)


def get_config(env, args):
    config_files = args["-c"]
    return Config(env, config_files[:-1], config_files[-1])


def main():
    args = docopt(__doc__)
    root_path = args['--root']
    env = Environment()
    env.ROOT_PATH = root_path
    tools = Tools(env)
    config = get_config(env, args)

    app = get_app()
    set_loop(app)
    loop = asyncio.get_event_loop()

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()

    http_session = aiohttp.ClientSession(loop=loop)
    lobby_server = LobbyServer(config["lobby_server"], tools)
    irc = Irc(config["irc_server"])
    resources = Resources(config["resources"], http_session)

    models = Models(config, lobby_server, irc)

    login_session = LoginSession(lobby_server, irc, models, ctx)
    qt_models = QtModels(models, resources)

    news = NewsTab(login_session, ctx)
    games = GamesTab(qt_models, ctx)
    chat = ChatTab(irc, models, ctx)

    qml_file = os.path.join(root_path, "res/ui/main_window/ToplevelWindow.qml")

    ctx.setContextProperty("ROOT_PATH", QUrl.fromLocalFile(env.ROOT_PATH))
    engine.load(qml_file)

    with loop:
        sys.exit(loop.run_forever())
