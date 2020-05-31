import sys
import os

from faf.session import LoginSession
from faf.tabs.news import NewsTab
from faf.tabs.games import GamesTab
from faf.tabs.chat import ChatTab
from faf.models import Models
from faf.qt_models import QtModels
from faf.environment import Environment

from test.mock.irc import MockIrc
from test.mock.lobbyserver import MockLobbyServer
from test.mock.resources import MockResources


class MockFAFClient:
    def __init__(self, env):
        self.env = env
        self.resources = MockResources()
        self.lobby_server = MockLobbyServer()
        self.irc = MockIrc()

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
    client = MockFAFClient(env)

    qml_file = os.path.join(env.paths.ROOT_PATH,
                            "res/ui/main_window/ToplevelWindow.qml")
    env.qml_engine.load(qml_file)

    with env.loop:
        sys.exit(env.loop.run_forever())


main()
