import asyncio
import os
from aiogram import Bot,Dispatcher, types
from aiogram.types import BotCommandScopeAllPrivateChats
from  dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

from database.models import async_main
from handlers import router

TOKEN = os.getenv('TOKEN')

async def on_shutdown(bot):
    print("бот лёг")


async def main():
    await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(skip_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)


asyncio.run(main())