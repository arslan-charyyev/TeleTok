from abc import ABC
from dataclasses import dataclass

from aiogram.utils.formatting import Bold, Text


class Tiktok(ABC):
    url: str
    description: str

    @property
    def caption(self) -> Text:
        return Text(f"{self.description}\n\n{self.url}")


@dataclass
class VideoTiktok(Tiktok):
    video: bytes


@dataclass
class PhotoTiktok(Tiktok):
    title: str
    photos: list[bytes]

    @property
    def caption(self) -> Text:
        return Text(Bold(self.title), "\n\n", super().caption)
