import sys
import os

print("=== RUN.PY STARTED ===", flush=True)
print(f"Python: {sys.version}", flush=True)
print(f"CWD: {os.getcwd()}", flush=True)
print(f"Files: {os.listdir('.')}", flush=True)

token = os.getenv("BOT_TOKEN", "")
print(f"BOT_TOKEN exists: {bool(token)}", flush=True)
print(f"BOT_TOKEN length: {len(token)}", flush=True)

if not token:
    print("FATAL: BOT_TOKEN is not set!", flush=True)
    sys.exit(1)

import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)

print("Importing aiogram...", flush=True)
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
print("aiogram OK", flush=True)

print("Importing handlers...", flush=True)
from handlers import all_routers
print(f"Routers: {len(all_routers)}", flush=True)

print("Importing db...", flush=True)
from database.db import init_db
print("DB OK", flush=True)

async def main():
    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    for router in all_routers:
        dp.include_router(router)
    init_db()
    print("=== BOT STARTING POLLING ===", flush=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())