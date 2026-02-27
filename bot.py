import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
import database as db
from handlers import all_routers

logging.basicConfig(level=logging.INFO)

if not config.BOT_TOKEN:
    raise ValueError("Нет токена!")

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

for router in all_routers:
    dp.include_router(router)

async def main():
    db.init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())