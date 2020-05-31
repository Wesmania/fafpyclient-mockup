import aiohttp
import json


class WordpressAPI:
    def __init__(self, config, aiohttp_session):
        self._http = aiohttp_session
        self._route = config["url"]

    # TODO log
    async def fetch(self, page=1, count=10):
        url = self._route.format(page=page, count=count)
        try:
            async with self._http.get(url) as reply:
                if reply.status != 200:
                    return None
                content = await reply.text()
                return self._process(content)
        except (aiohttp.ClientError, IOError):
            return None

    def _process(self, content):
        try:
            js = json.loads(bytes(content).decode('utf-8'))
            posts = []
            for post in js:
                content = {
                    'title': post.get('title', {}).get('rendered', ""),
                    'body': post.get('content', {}).get('rendered', ""),
                    'date': post.get('date'),
                    'excerpt': post.get('excerpt', {}).get('rendered', ""),
                    'author': post.get('_embedded', {}).get('author', [])
                }
                posts.append(content)
            return posts
        except Exception:
            return None
