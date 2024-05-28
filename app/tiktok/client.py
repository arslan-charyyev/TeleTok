import json
import random
import string
from datetime import UTC, datetime

import httpx
from bs4 import BeautifulSoup
from httpx import URL

from settings import settings
from tiktok.source import PhotoSource, Source, VideoSource
from utils import DifferentPageError, NoDataError, NoScriptError, SignTokError, retries


class AsyncTikTokClient(httpx.AsyncClient):
    def __init__(self) -> None:
        super().__init__(
            headers={
                "Referer": "https://www.tiktok.com/",
                "User-Agent": (
                    f"{''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 10)))}-"
                    f"{''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 7)))}/"
                    f"{random.randint(10, 300)} "
                    f"({datetime.now(tz=UTC).replace(microsecond=0).timestamp()})"
                ),
            },
            timeout=30,
            cookies={
                "tt_webid_v2": f"{random.randint(10 ** 18, (10 ** 19) - 1)}",
            },
            follow_redirects=True,
        )

    @retries(times=3)
    async def get_page_data(self, url: str) -> Source:
        page = await self.get(url)
        page_id = page.url.path.rsplit("/", 1)[-1]

        soup = BeautifulSoup(page.text, "html.parser")

        if script := soup.select_one('script[id="__UNIVERSAL_DATA_FOR_REHYDRATION__"]'):
            script = json.loads(script.text)
        else:
            raise NoScriptError

        source: Source

        if video_detail := script["__DEFAULT_SCOPE__"].get("webapp.video-detail"):
            try:
                item_struct = video_detail["itemInfo"]["itemStruct"]
            except KeyError as ex:
                raise NoDataError from ex

            if item_struct["id"] != page_id:
                raise DifferentPageError

            source = VideoSource(item_struct)
        elif settings.signtok_url:
            unsigned_url = URL(
                "https://www.tiktok.com/api/item/detail/",
                params={
                    "itemId": page_id,
                    "aid": 1998,
                    "app_language": "en",
                    "app_name": "tiktok_web",
                    "browser_language": "en-US",
                    "browser_name": "Mozilla",
                    "browser_platform": "Win32",
                    "browser_version": "4.0",
                    "device_id": "1234567890123456789",
                    "device_platform": "web_pc",
                    "os": "windows",
                    "region": "US",
                    "screen_height": 720,
                    "screen_width": 1280,
                    "webcast_language": "en",
                },
            )

            res = await self.post(settings.signtok_url, content=str(unsigned_url))

            if not res.is_success or (res_json := res.json())["status"] != "ok":
                raise SignTokError

            signed_url = res_json["data"]["signed_url"]
            user_agent = res_json["data"]["navigator"]["user_agent"]

            item_detail_res = await self.get(signed_url, headers={"User-Agent": user_agent})

            try:
                item_struct = item_detail_res.json()["itemInfo"]["itemStruct"]
            except KeyError as ex:
                raise NoDataError from ex

            source = PhotoSource(item_struct)
        else:
            raise NoDataError

        return source

    async def get_content(self, url: str) -> bytes:
        res = await self.get(url)
        return res.content
