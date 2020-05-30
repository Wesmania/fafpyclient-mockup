from faf.session.login import LoginProcess, LobbyLogin


class LoginSessionData:
    def __init__(self, model_player_updater):
        self._model_player_updater = model_player_updater

        self.player = None
        self.password = None

    def load_from_login_msg(self, msg):
        pinfo = msg.player_info
        self.player = self._model_player_updater.add_player_from_msg(pinfo)
        self.password = msg.password

    def reset(self):
        self.player = None
        self.password = None


class LogoutModelCleaner:
    def __init__(self, models, login):
        self._models = models
        self._login = login
        login.logged_out.connect(self._clear_models)

    def _clear_models(self):
        self._models.games.clear()
        self._models.players.clear()
        self._models.current_player_game.clear()
        self._models.chat.clear()

        self._models.games.cleared.on_next(None)
        self._models.players.cleared.on_next(None)
        self._models.chat.cleared.on_next(None)


class LoginSession:
    def __init__(self, lobby_server, irc, models, qml_context):
        self.login_process = LoginProcess(lobby_server)
        self.session = LoginSessionData(models.control.player_updater)
        self.login = LobbyLogin(self.login_process, self.session)
        self._model_cleaner = LogoutModelCleaner(models.data, self.login)
        qml_context.setContextProperty("faf__session__login", self.login)

        # FIXME find a better spot for this, plus reconnecting
        self._irc = irc
        self.login.logged_in.connect(self._irc_connect)
        self.login.logged_out.connect(self._irc_disconnect)

    def _irc_connect(self):
        self._irc.client.connect_(self.session.player.login,
                                  self.session.password)

    def _irc_disconnect(self):
        self._irc.client.disconnect_()
