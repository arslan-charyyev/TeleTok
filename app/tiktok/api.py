import asyncio
from collections.abc import AsyncIterable

from tiktok.client import AsyncTikTokClient
from tiktok.data import PhotoTiktok, Tiktok, VideoTiktok
from tiktok.source import PhotoSource, VideoSource


class TikTokAPI:
    @classmethod
    async def download_tiktoks(cls, urls: list[str]) -> AsyncIterable[Tiktok]:
        tasks = [cls.download_tiktok(url) for url in urls]
        for task in asyncio.as_completed(tasks):
            tiktok = await task
            yield tiktok

    @classmethod
    async def download_tiktok(cls, url: str) -> Tiktok:
        async with AsyncTikTokClient() as client:
            source = await client.get_page_data(url)
            tiktok: Tiktok

            if isinstance(source, VideoSource):
                video = await client.get_content(url=source.url)
                tiktok = VideoTiktok(video)
            elif isinstance(source, PhotoSource):
                photos = [await client.get_content(url=url) for url in source.urls]
                tiktok = PhotoTiktok(title=source.title, photos=photos)
            else:
                raise NotImplementedError

            tiktok.url = url
            tiktok.description = source.description

            return tiktok
