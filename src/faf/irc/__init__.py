from faf.irc.irc import IrcClient


class Irc:
    def __init__(self, config):
        self.client = IrcClient(config["host"], config["port"])
        self.client.at_nickserv_identified.connect(self.on_identified)

    def on_identified(self):
        print("TODO: autojoin channels")
