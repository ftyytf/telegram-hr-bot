import asyncio
import sys
import os

print("=== RUN.PY STARTED ===", flush=True)
print(f"Python: {sys.version}", flush=True)

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.db import init_db

from handlers.start import router as start_router
from handlers.log_event import router as log_router
from handlers.analytics import router as analytics_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(log_router)
dp.include_router(analytics_router)

async def main():
    print("=== INIT DB ===", flush=True)
    await init_db()
    print("=== DB READY, STARTING POLLING ===", flush=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
