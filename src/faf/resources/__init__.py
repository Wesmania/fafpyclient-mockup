from faf.resources.images import ImageCache


class Resources:
    def __init__(self, config, http_session):
        mp = config['map_previews']
        self.map_previews = ImageCache(mp['cache_dir'], mp['access_url'],
                                       mp['default_image'], http_session)
