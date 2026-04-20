import asyncio
import logging
import os
from aiohttp import web
from bot import bot, dp
from database.db import init_db
from web_app import create_app


async def main():
    logging.info("Инициализация базы данных...")
    await init_db()

    # Web server
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Web server started on port {port}")

    # Bot
    logging.info("Бот запускается...")
    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
