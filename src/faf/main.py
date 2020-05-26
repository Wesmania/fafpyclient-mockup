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
from faf.tools import glob


def get_app():
    args = [sys.argv[0], "--style", "Material"]
    QtWebEngine.initialize()
    return QGuiApplication(args)


def set_loop(app):
    # Asyncqt and kin are broken with the proactor loop on Windows
    loop = QSelectorEventLoop(app)
    asyncio.set_event_loop(loop)


def get_config(args):
    config_files = args["-c"]
    return Config(config_files[:-1], config_files[-1])


def main():
    args = docopt(__doc__)
    config = get_config(args)
    root_path = args['--root']
    glob.ROOT_PATH = root_path

    app = get_app()
    set_loop(app)
    loop = asyncio.get_event_loop()

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()

    http_session = aiohttp.ClientSession(loop=loop)
    lobby_server = LobbyServer(config["lobby_server"])
    irc = Irc(config["irc_server"])
    resources = Resources(config["resources"], http_session)

    models = Models(config, lobby_server, irc)

    login_session = LoginSession(lobby_server, irc, models, ctx)
    qt_models = QtModels(models, resources)

    news = NewsTab(login_session, ctx)
    games = GamesTab(qt_models, ctx)
    chat = ChatTab(irc, models, ctx)

    qml_file = os.path.join(root_path, "res/ui/main_window/ToplevelWindow.qml")

    ctx.setContextProperty("ROOT_PATH", f"file:///{root_path}")
    engine.load(qml_file)

    with loop:
        sys.exit(loop.run_forever())
