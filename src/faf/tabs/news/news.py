from PySide2.QtCore import QObject, Slot

from faf.tabs.news.wpapi import WPAPI
from faf.qt import QtListModel


class NewsModel(QtListModel):
    @Slot(int, result='QVariant')
    def news_contents(self, idx):
        try:
            item = self._items[idx]
        except IndexError:
            return {'title': '', 'body': ''}
        return item

    def set_news(self, items):
        self._set_list(items)


class NewsTab(QObject):
    def __init__(self, login_session, qml_context):
        QObject.__init__(self)
        self._login_session = login_session
        self._api = WPAPI()
        self.model = NewsModel()

        self._login_session.login.logged_in.connect(self.fetch)
        self._api.done.connect(self._set_news)

        qml_context.setContextProperty("faf__tabs__news", self)
        qml_context.setContextProperty("faf__tabs__news__model", self.model)

    @Slot()
    def fetch(self):
        self._api.fetch()

    def _set_news(self, news_list):
        self.model.set_news(news_list)
