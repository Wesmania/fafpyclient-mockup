from dataclasses import dataclass


@dataclass
class Map:
    id: str
    name: str
    folder_name: str
    description: str
    number_of_plays: int
    downloads: int
    players: int
    size: object
    version: object
    small_thumb_url: str
    large_thumb_url: str
    download_url: str
    author: str
    creation_time: int
    type: object
    reviews: list
    hidden: bool
    ranked: bool
