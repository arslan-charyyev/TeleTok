from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import (
    BufferedInputFile,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)

from settings import settings
from tiktok.api import TikTokAPI
from tiktok.data import PhotoTiktok, VideoTiktok

dp = Dispatcher()

filters = [
    F.text.contains("tiktok.com"),
    (not settings.allowed_ids)
    | F.chat.id.in_(settings.allowed_ids)
    | F.from_user.id.in_(settings.allowed_ids),
]

# Needed to fix mypy error
Media = list[InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo]


@dp.message(*filters)
@dp.channel_post(*filters)
async def handle_tiktok_request(message: Message, bot: Bot) -> None:
    entries = [
        message.text[e.offset : e.offset + e.length]
        for e in message.entities or []
        if message.text is not None
    ]

    urls = [
        u if u.startswith("http") else f"https://{u}"
        for u in filter(lambda e: "tiktok.com" in e, entries)
    ]

    async for tiktok in TikTokAPI.download_tiktoks(urls):
        chat_id = message.chat.id
        reply_to_message_id = message.message_id if settings.reply_to_message else None
        caption = tiktok.caption.as_markdown() if settings.with_captions else None
        parse_mode = ParseMode.MARKDOWN_V2
        disable_notification = settings.disable_notification

        if isinstance(tiktok, VideoTiktok):
            video = BufferedInputFile(tiktok.video, filename="video.mp4")

            await bot.send_video(
                chat_id=chat_id,
                video=video,
                caption=caption,
                parse_mode=parse_mode,
                reply_to_message_id=reply_to_message_id,
                disable_notification=disable_notification,
            )
        elif isinstance(tiktok, PhotoTiktok):
            first_with_caption = InputMediaPhoto(
                media=BufferedInputFile(tiktok.photos[0], filename="image"),
                caption=caption,
                parse_mode=parse_mode,
            )

            rest_without_captions = [
                InputMediaPhoto(media=BufferedInputFile(photo, filename="image"))
                for photo in tiktok.photos[1:]
            ]

            photos: Media = [first_with_caption, *rest_without_captions]

            # Can send up to 10 photos max, so we split the photos into batches
            image_count = 10
            for n in range(0, len(tiktok.photos), image_count):
                await bot.send_media_group(
                    chat_id=chat_id,
                    media=photos[n : n + image_count],
                    reply_to_message_id=reply_to_message_id,
                    disable_notification=disable_notification,
                )
