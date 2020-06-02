from PySide2.QtCore import QObject, Signal, QUrl
import os


class MockWordpressAPI:
    async def fetch(self, page=1, count=10):
        return [{
            'title': f'Page {page} title {i}',
            'body': f'Page {page} content {i}',
            'date': '2020-05-25T22:06:00',
            'excerpt': 'stuff {i}',
            'author': "foobar",
        } for i in range(count)]


class MockImageCache(QObject):
    image_available = Signal(object)

    def __init__(self, env):
        QObject.__init__(self)
        self._env = env

    def get(self, key):
        tmp = os.path.join(self._env.paths.ROOT_PATH,
                           "res/icons/games/unknown_map.png")
        return QUrl.fromLocalFile(tmp)


class MockResources:
    def __init__(self, env):
        self.wordpress_api = MockWordpressAPI()
        self.map_previews = MockImageCache(env)
