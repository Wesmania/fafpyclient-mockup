from PySide2.QtCore import QObject, Slot
import asyncio
from faf.qt import QtPlainListModel, QtRoleEnum


class NewsRoles(QtRoleEnum):
    news_title = ()
    news_body = ()


class NewsModel(QtPlainListModel):
    @Slot(int, result='QVariant')
    def news_contents(self, idx):
        try:
            item = self._itemlist[idx]
        except IndexError:
            return {'title': '', 'body': ''}
        return item

    def role(self, item, role):
        role = NewsRoles(role)
        if role is NewsRoles.news_title:
            return item['title']
        elif role is NewsRoles.news_body:
            return item['body']

    def roleNames(self):
        return NewsRoles.role_names()

    def set_news(self, items):
        self._set_list(items)


class NewsTab(QObject):
    def __init__(self, login_session, resources, qml_context):
        QObject.__init__(self)
        self._login_session = login_session
        self._api = resources.wordpress_api
        self.model = NewsModel()
        self._fetch_job = None

        self._login_session.login.logged_in.connect(self.fetch)

        qml_context.setContextProperty("faf__tabs__news", self)
        qml_context.setContextProperty("faf__tabs__news__model", self.model)

    @Slot()
    def fetch(self):
        if self._fetch_job is not None and not self._fetch_job.done():
            return
        self._fetch_job = asyncio.create_task(self._fetch())
        self._fetch_job.add_done_callback(lambda f: None)

    async def _fetch(self):
        news = await self._api.fetch()
        if news is not None:
            self.model.set_news(news)
