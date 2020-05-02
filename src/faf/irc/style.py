# This bit was taken from PyPi ircmessage module, on Apache license.
# Thanks, Makoto Fujimoto!
import re


NORMAL = "\x0F"
BOLD = "\x02"
ITALICS = "\x1D"
UNDERLINE = "\x1F"
COLOR = "\x03"


def unstyle(text):
    # Strip attribute codes first
    for code in (NORMAL, BOLD, ITALICS, UNDERLINE):
        text = text.replace(code, '')

    text = re.sub('\x03(?P<fg>\\d{2})(,(?P<bg>\\d{2}))?', '', text)

    return text
