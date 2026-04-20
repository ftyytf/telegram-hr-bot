from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import DEFAULT_CATEGORIES, STATUSES


def main_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Заполнить день", callback_data="fill_day")],
        [InlineKeyboardButton(text="Мой день сейчас", callback_data="show_day")],
        [InlineKeyboardButton(text="Рекомендация", callback_data="recommend")],
        [InlineKeyboardButton(text="Статистика за неделю", callback_data="stats_week")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def categories_kb(entry: dict) -> InlineKeyboardMarkup:
    buttons = []
    for cat in DEFAULT_CATEGORIES:
        status = entry.get(cat["key"], "none")
        status_icon = ""
        if status == "yes":
            status_icon = " ✅"
        elif status == "partial":
            status_icon = " 🟡"
        elif status == "no":
            status_icon = " ❌"

        buttons.append([
            InlineKeyboardButton(
                text=f'{cat["emoji"]} {cat["name"]}{status_icon}',
                callback_data=f'cat_{cat["key"]}',
            )
        ])

    buttons.append([InlineKeyboardButton(text="💬 Добавить заметку", callback_data="add_note")])
    buttons.append([InlineKeyboardButton(text="✅ Завершить день", callback_data="finish_day")])
    buttons.append([InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def status_kb(category_key: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="✅ Да", callback_data=f"st_{category_key}_yes"),
            InlineKeyboardButton(text="🟡 Частично", callback_data=f"st_{category_key}_partial"),
            InlineKeyboardButton(text="❌ Нет", callback_data=f"st_{category_key}_no"),
        ],
        [InlineKeyboardButton(text="🔙 Назад к категориям", callback_data="fill_day")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
