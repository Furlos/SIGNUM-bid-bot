import asyncio

from aiogram import Bot, Dispatcher

from handlers import main_router
from config import token
async def main():
    bot = Bot(token=token)
    db = Dispatcher()
    db.include_router(main_router)
    await db.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())