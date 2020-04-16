from PySide2.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide2.QtCore import QObject, QUrl, Signal
from collections import namedtuple
import json


from PySide2.QtCore import qDebug


# FIXME: Make setting
WPAPI_ROOT = 'http://direct.faforever.com/wp-json/wp/v2/posts?per_page={perpage}&page={page}&_embed=1'


class WPAPI(QObject):
    done = Signal(list)

    def __init__(self):
        QObject.__init__(self)
        self._nam = QNetworkAccessManager(self)
        self._nam.finished.connect(self._on_fetched)

    def fetch(self, page=1, perpage=10):
        url = QUrl(WPAPI_ROOT.format(page=page, perpage=perpage))
        request = QNetworkRequest(url)
        self._nam.get(request)

    def _on_fetched(self, reply):
        content = reply.readAll()
        try:
            js = json.loads(bytes(content).decode('utf-8'))
            posts = []
            for post in js:
                content = {
                    'title': post.get('title', {}).get('rendered'),
                    'body': post.get('content', {}).get('rendered'),
                    'date': post.get('date'),
                    'excerpt': post.get('excerpt', {}).get('rendered'),
                    'author': post.get('_embedded', {}).get('author')
                }
                posts.append(content)
            self.done.emit(posts)
        except Exception:
            pass
