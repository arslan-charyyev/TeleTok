import asyncio
import logging

from aiogram import Bot

from bot import dp
from settings import settings


async def start() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.api_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
