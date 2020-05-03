import time


class ChatLine:
    def __init__(self, chatter, message, type_, timestamp=None):
        self.nick = chatter.nick
        self.message = message
        if timestamp is None:
            timestamp = time.time()
        self.time = timestamp
        self.type = type_

        self.clan = None
        self.avatar = None

        self.is_mod = False
        self.is_friend = False
        self.is_foe = False
        self.is_clannie = False
        self.is_me = False

        self.mentions_me = False

        # TODO - fill attributes
        # self.is_mod = chatter.is_mod()

        if chatter.player is not None:
            self._fill_player_info(chatter.player)

    def _fill_player_info(self, player):
        pass    # TODO
