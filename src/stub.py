import sys
import os

from faf.session import LoginSession
from faf.tabs.news import NewsTab
from faf.tabs.games import GamesTab
from faf.tabs.chat import ChatTab
from faf.models import Models
from faf.qt_models import QtModels
from faf.environment import Environment
from faf.lobbyserver.connection import ConnectionState
from faf.models.data.game import GameState, GameVisibility

from test.mock.irc import MockIrc
from test.mock.lobbyserver import MockLobbyServer
from test.mock.resources import MockResources


class MockFAFClient:
    def __init__(self, env):
        self.env = env
        self.resources = MockResources(self.env)
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

        self.lobby_server.obs_connection_state.subscribe(self._on_connected)

    def _on_connected(self, state):
        if state is not ConnectionState.CONNECTED:
            return

        def player(i):
            no_ava = os.path.join(self.env.paths.ROOT_PATH,
                                  "res/icons/chat/no_avatar.png")
            no_ava = os.path.realpath(no_ava)
            return {
                'id': 1,
                'login': f'foobar{i}',
                'global_rating': [1500.00, 500.00],
                'ladder_rating': [1500.00, 500.00],
                'number_of_games': 500,
                'avatar': {
                    'url': f"file:///{no_ava}",
                    'tooltip': 'foobar'
                },
                'country': 'EN'
            }

        for i in range(1, 100):
            self.lobby_server.player_msg.new.on_next(player(i))

        def game(i):
            return {
                'command': 'game_info',
                'visibility': GameVisibility.PUBLIC,
                'password_protected': False,
                'uid': i,
                'title': f'Game {i}',
                'state': GameState.OPEN,
                'featured_mod': 'faf',
                'sim_mods': {},
                'mapname': f'Placeholder{i}',
                'map_file_path': f'maps/placeholder{i}.zip',
                'host': f'foobar{3*i+1}',
                'num_players': 3,
                'max_players': 3,
                'launched_at': None,
                'teams': {
                    '2': [f'foobar{3*i+1}', f'foobar{3*i+2}'],
                    '3': [f'foobar{3*i+3}'],
                },
            }

        for i in range(1, 10):
            self.lobby_server.game_msg.new.on_next(game(i))


def main():
    env = Environment(sys.argv)
    client = MockFAFClient(env)

    qml_file = os.path.join(env.paths.ROOT_PATH,
                            "res/ui/main_window/ToplevelWindow.qml")
    env.qml_engine.load(qml_file)

    with env.loop:
        sys.exit(env.loop.run_forever())


main()
