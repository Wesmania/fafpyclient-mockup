from faf.resources.images import ImageCache
from faf.resources.news_feed import WordpressAPI


class Resources:
    def __init__(self, config, http_session):
        mp = config['map_previews']
        self.map_previews = ImageCache(mp['cache_dir'], mp['access_url'],
                                       mp['default_image'], http_session)
        self.wordpress_api = WordpressAPI(config['news_feed'], http_session)
