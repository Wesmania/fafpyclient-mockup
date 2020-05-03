import re
from faf.irc.irc import MessageType


class IrcControl:
    def __init__(self, irc_client, chat_model_ctl):
        self._irc_client = irc_client
        self._chat_model_ctl = chat_model_ctl

    def send(self, target, message, type_: MessageType):
        if type_ is MessageType.MESSAGE:
            self._irc_client.send_privmsg(target, message)
        elif type_ is MessageType.NOTICE:
            self._irc_client.send_notice(target, message)
        elif type_ is MessageType.ACTION:
            self._irc_client.send_action(target, message)

    def join(self, target):
        self._irc_client.join(target)

    def join_priv(self, chatter):
        self._chat_model_ctl.join_private_channel(chatter)

    def part(self, target, is_public):
        if is_public:
            self._irc_client.part(target)
        else:
            self._chat_model_ctl.leave_private_channel(target)

    def topic(self, channel, message):
        self._irc_client.topic(channel, message)


class IrcLineParser:
    def __init__(self, control):
        self._control = control

    def handle_line(self, line, target):
        # Filter wacky whitespace and multiline messages.
        line = line.split("\n")[0]
        line = re.sub("\\s", " ", line).strip()
        if not line:
            return

        if line.startswith("/join "):
            rest = line[6:].split(" ")[0]
            self._control.join(rest)
        elif line.startswith("/msg "):
            rest = line[5:].split(" ", 1)
            if len(rest) < 2:
                return
            target, msg = rest
            self._control.send(target, msg, MessageType.MESSAGE)
        elif line.startswith("/topic "):
            rest = line[7:].split(" ", 1)
            if len(rest) < 2:
                return
            target, msg = rest
            self._control.topic(target, msg)
        elif line.startswith("/me "):
            if target is None:
                return
            rest = line[4:]
            self._control.send(target, rest, MessageType.ACTION)
        else:
            if target is None:
                return
            self._control.send(target, line, MessageType.MESSAGE)
