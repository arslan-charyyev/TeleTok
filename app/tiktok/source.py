from abc import ABC
from dataclasses import dataclass


class Source(ABC):
    description: str


@dataclass
class VideoSource(Source):
    url: str

    def __init__(self, item_struct: dict) -> None:
        self.description = item_struct["desc"]
        self.url = item_struct["video"].get("playAddr") or item_struct["video"].get("downloadAddr")


@dataclass
class PhotoSource(Source):
    title: str
    urls: list[str]

    def __init__(self, item_struct: dict) -> None:
        self.title = item_struct["imagePost"]["title"]
        self.description = " ".join([content["desc"] for content in item_struct["contents"]])
        self.urls = [
            image["imageURL"]["urlList"][0] for image in item_struct["imagePost"]["images"]
        ]
