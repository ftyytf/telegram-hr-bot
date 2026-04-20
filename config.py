import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))

# Категории трекера по умолчанию
DEFAULT_CATEGORIES = [
    {"key": "sleep", "name": "Сон", "emoji": "\U0001f634"},
    {"key": "work", "name": "Главная рабочая задача", "emoji": "\U0001f4bc"},
    {"key": "growth", "name": "Развитие", "emoji": "\U0001f4da"},
    {"key": "sport", "name": "Движение / спорт", "emoji": "\U0001f3c3"},
    {"key": "finance", "name": "Финансовая осознанность", "emoji": "\U0001f4b0"},
    {"key": "no_chaos", "name": "Без хаоса / самосаботажа", "emoji": "\U0001f9d8"},
    {"key": "joy", "name": "Живой момент / удовольствие", "emoji": "\U0001f31f"},
]

# Статусы категорий
STATUSES = {
    "yes": "\u2705 Да",
    "partial": "\U0001f7e1 Частично",
    "no": "\u274c Нет",
    "none": "\u2b1c Не отмечено",
}

DB_PATH = "bot_data.db"
