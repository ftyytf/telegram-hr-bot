import asyncio
import logging
import sys
from bot import bot, dp
from database.db import init_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)


async def main():
    logging.info("Инициализация базы данных...")
    await init_db()
    logging.info("Бот запускается...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
