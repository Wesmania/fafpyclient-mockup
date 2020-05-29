"""FAF client.

Usage:
  main.py --root <root_dir> -c <files>...

Options:
  -c <files>...   Configuration files to use. Last one is treated as user-writable config file.
  --root <root_dir> Root resource directory.
"""

from dataclasses import dataclass
import asyncio
import aiohttp
from asyncqt import QSelectorEventLoop
from docopt import docopt

from PySide2.QtCore import QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWebEngine import QtWebEngine

from faf.config import Config
from faf.tools import Tools


@dataclass
class Paths:
    ROOT_PATH: str = None


class Environment:
    def __init__(self, argv):
        self._docopt = docopt(__doc__)
        self.paths = Paths()
        self.paths.ROOT_PATH = self._docopt["--root"]
        self.tools = Tools(self.paths)
        self.config = self._get_config()
        self.qapp = self._get_app(argv)
        self._set_loop()
        self.aiohttp_session = aiohttp.ClientSession(loop=self.loop)
        self.qml_engine = QQmlApplicationEngine()
        self.qml_engine_ctx = self.qml_engine.rootContext()
        self.qml_engine_ctx.setContextProperty(
            "ROOT_PATH", QUrl.fromLocalFile(self.paths.ROOT_PATH))

    def _get_app(self, argv):
        args = [argv[0], "--style", "Material"]
        QtWebEngine.initialize()
        return QGuiApplication(args)

    def _set_loop(self):
        # Asyncqt and kin are broken with the proactor loop on Windows
        self.loop = QSelectorEventLoop(self.qapp)
        asyncio.set_event_loop(self.loop)

    def _get_config(self):
        config_files = self._docopt["-c"]
        return Config(self.paths, config_files[:-1], config_files[-1])
