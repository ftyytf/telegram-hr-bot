import sys
print("Python started", flush=True)
print(f"Python version: {sys.version}", flush=True)

try:
    print("Importing bot...", flush=True)
    from bot import bot, dp
    print("Bot imported OK", flush=True)
except Exception as e:
    print(f"IMPORT ERROR: {e}", flush=True)
    sys.exit(1)

try:
    print("Importing handlers...", flush=True)
    from handlers import setup_routers
    print("Handlers imported OK", flush=True)
except Exception as e:
    print(f"HANDLERS IMPORT ERROR: {e}", flush=True)
    sys.exit(1)

try:
    print("Importing db...", flush=True)
    from database.db import init_db
    print("DB imported OK", flush=True)
except Exception as e:
    print(f"DB IMPORT ERROR: {e}", flush=True)
    sys.exit(1)

import asyncio

async def main():
    print("Setting up routers...", flush=True)
    setup_routers(dp)
    print("Initializing database...", flush=True)
    init_db()
    print("Bot starting polling...", flush=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
