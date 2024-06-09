from abc import ABC
from dataclasses import dataclass

from aiogram.utils.formatting import Bold, Text

from settings import settings


class Tiktok(ABC):
    url: str
    description: str

    @property
    def _caption_text(self) -> str:
        gap = "\n\n" if self.description else ""
        footer = "" if settings.reply_to_message else f"{gap}{self.url}"
        return f"{self.description}{footer}"

    @property
    def caption(self) -> Text:
        return Text(self._caption_text)


@dataclass
class VideoTiktok(Tiktok):
    video: bytes


@dataclass
class PhotoTiktok(Tiktok):
    title: str
    photos: list[bytes]

    @property
    def caption(self) -> Text:
        header = Bold(self.title) if self.title and (self.title != self.description) else ""
        gap = "\n\n" if header else ""
        return Text(header, gap, self._caption_text)
