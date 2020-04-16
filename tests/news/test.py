import sys
import os
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWebEngine import QtWebEngine
from news.news import News


def get_app():
    sys.argv += ["--style", "Material"]
    QtWebEngine.initialize()
    return QGuiApplication(sys.argv)


if __name__ == "__main__":
    app = get_app()

    news = News.build()

    root_path = os.path.join(os.path.dirname(__file__), "../..")
    qml_file = os.path.join(root_path, "tests/news/TestNews.qml")

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("ROOT_PATH", root_path)
    ctx.setContextProperty("news", news)
    ctx.setContextProperty("news_model", news.model)
    engine.load(qml_file)

    sys.exit(app.exec_())
