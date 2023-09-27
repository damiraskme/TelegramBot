import logging
import asyncio
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode

from addition.basic_func import get_apikey
from messages.bot_start import router_start
from messages.bot_tiktok import router_tiktok
from messages.bot_calendar import router_calendar
from messages.bot_youtube import router_youtube
from messages.bot_download import router_download



API_TOKEN = get_apikey()
logging.basicConfig(level=logging.INFO)

main_router = Router()


@main_router.message(Command("info"))
async def info_send(message: types.Message):
    await message.reply("Bot made by me!")

async def main():
    bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_router)
    dp.include_routers(router_start, router_tiktok, router_calendar, router_youtube, router_download)

    await dp.start_polling(bot)

if __name__ == '__main__':
    # Setup_start
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())