from faf.resources.images import ImageCache
import os


class Resources:
    def __init__(self, config, http_session):
        mp = config['map_previews']
        cache_dir = os.path.realpath(mp['cache_dir'])
        access_url = os.path.realpath(mp['access_url'])
        default_image = os.path.realpath(mp['default_image'])
        self.map_previews = ImageCache(cache_dir, access_url, default_image,
                                       http_session)
