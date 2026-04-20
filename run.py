import asyncio
import sys
import os

print("=== RUN.PY STARTED ===", flush=True)
print(f"Python: {sys.version}", flush=True)

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.db import init_db
from web_app import create_app
from aiohttp import web

from handlers.start import router as start_router
from handlers.tracker import router as tracker_router
from handlers.stats import router as stats_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(tracker_router)
dp.include_router(stats_router)

async def main():
    print("=== INIT DB ===", flush=True)
    await init_db()
    print("=== DB READY ===", flush=True)

    # Запускаем веб-сервер на порту 8080
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("=== WEB SERVER STARTED ON PORT 8080 ===", flush=True)

    # Запускаем бота
    print("=== STARTING BOT POLLING ===", flush=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
