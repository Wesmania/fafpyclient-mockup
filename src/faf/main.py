"""FAF client.

Usage:
  main.py --root <root_dir> -c <files>...

Options:
  -c <files>...   Configuration files to use. Last one is treated as user-writable config file.
  --root <root_dir> Root resource directory.
"""

import sys
import os

from faf.lobbyserver import LobbyServer
from faf.session import LoginSession
from faf.tabs.news import NewsTab
from faf.tabs.games import GamesTab
from faf.tabs.chat import ChatTab
from faf.models import Models
from faf.resources import Resources
from faf.qt_models import QtModels
from faf.irc import Irc
from faf.environment import Environment


def main():
    env = Environment(sys.argv)

    lobby_server = LobbyServer(env.config["lobby_server"], env.tools)
    irc = Irc(env.config["irc_server"])
    resources = Resources(env.config["resources"], env.aiohttp_session)

    models = Models(env.config, lobby_server, irc)

    login_session = LoginSession(lobby_server, irc, models, env.qml_engine_ctx)
    qt_models = QtModels(models, resources)

    news = NewsTab(login_session, env.qml_engine_ctx)
    games = GamesTab(qt_models, env.qml_engine_ctx)
    chat = ChatTab(irc, models, env.qml_engine_ctx)

    qml_file = os.path.join(env.paths.ROOT_PATH,
                            "res/ui/main_window/ToplevelWindow.qml")
    env.qml_engine.load(qml_file)

    with env.loop:
        sys.exit(env.loop.run_forever())
