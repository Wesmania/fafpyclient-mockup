import asyncio
import aiohttp
from PySide2.QtCore import QObject, Signal, QUrl
from PySide2.QtGui import QPixmap


class FutureImage(QObject):
    available = Signal(object)

    def __init__(self, key, filename, url, http_session):
        QObject.__init__(self)
        self._key = key
        self._filename = filename
        self._url = url
        self._http = http_session

        self.image = QPixmap(self._filename)
        if not self.image:
            loop = asyncio.get_event_loop()
            self._download_task = loop.create_task(self._load())

    async def _load(self):
        try:
            async with self._http.get(self._url) as reply:
                if reply.status != 200:
                    self._avail_future.set_result(None)
                    return
                with open(self._filename, "wb") as f:
                    while True:
                        chunk = await reply.content.read(65536)
                        if not chunk:
                            break
                        f.write(chunk)
            self.image = QPixmap(self._filename)
            self.available.emit(self._key)
        except (aiohttp.ClientError, IOError):
            pass    # TODO


class ImageCache(QObject):
    image_available = Signal(object)

    def __init__(self, cache_dir, access_url, default_image, http_session):
        QObject.__init__(self)
        self._cache_dir = cache_dir
        self._access_url = access_url
        self._images = {}
        self._http_session = http_session
        self._default_image = default_image

    def _img_file(self, name):
        return self._cache_dir.format(name=name)

    def _img_url(self, name):
        return self._access_url.format(name=name)

    def get(self, key):
        img = self._images.get(key)
        if img is None:
            img = FutureImage(key, self._img_file(key), self._img_url(key),
                              self._http_session)
            self._images[key] = img
            img.available.connect(self._on_new_img)
        if img.image:
            return QUrl.fromLocalFile(img._filename)
        else:
            return QUrl.fromLocalFile(self._default_image)

    def _on_new_img(self, key):
        self.image_available.emit(key)
