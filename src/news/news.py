from PySide2.QtCore import QObject, Slot

from news.wpapi import WPAPI
from qt.model import QListModel


class NewsModel(QListModel):
    @Slot(int, result='QVariant')
    def news_contents(self, idx):
        try:
            item = self.items[idx]
        except IndexError:
            return {'title': '', 'body': ''}
        return item


class News(QObject):
    def __init__(self, api, model):
        QObject.__init__(self)
        self._api = api
        self.model = model

        self._api.done.connect(self._set_news)

    @classmethod
    def build(cls):
        api = WPAPI()
        model = NewsModel()
        return cls(api, model)

    @Slot()
    def fetch(self):
        self._api.fetch()

    def _set_news(self, news_list):
        self.model.set(news_list)
