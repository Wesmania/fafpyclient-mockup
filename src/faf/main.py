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


class FAFClient:
    def __init__(self, env):
        self.env = env
        self.resources = Resources(self.env.config["resources"],
                                   self.env.aiohttp_session)
        self.lobby_server = LobbyServer(self.env.config["lobby_server"],
                                        self.env.tools)
        self.irc = Irc(self.env.config["irc_server"])

        self.models = Models(self.env.config, self.lobby_server, self.irc)
        self.qt_models = QtModels(self.models, self.resources)

        self.login_session = LoginSession(self.lobby_server, self.irc,
                                          self.models, self.env.qml_engine_ctx)

        self.news_tab = NewsTab(self.login_session, self.resources,
                                self.env.qml_engine_ctx)
        self.games_tab = GamesTab(self.qt_models, self.env.qml_engine_ctx)
        self.chat_tab = ChatTab(self.irc, self.models, self.env.qml_engine_ctx)


def main():
    env = Environment(sys.argv)
    client = FAFClient(env)

    qml_file = os.path.join(env.paths.ROOT_PATH,
                            "res/ui/main_window/ToplevelWindow.qml")
    env.qml_engine.load(qml_file)

    with env.loop:
        sys.exit(env.loop.run_forever())
