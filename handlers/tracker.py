from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import date

from database import get_or_create_entry, update_category, update_note, update_score
from keyboards import categories_kb, status_kb, main_menu_kb
from services import format_entry_summary, get_recommendation, calc_day_score

router = Router()

CATEGORY_KEYS = ["sleep", "work", "growth", "sport", "finance", "no_chaos", "joy"]


class NoteState(StatesGroup):
    waiting_for_note = State()


def parse_status_callback(data: str):
    """Парсит callback вида st_<category>_<status>.
    Корректно обрабатывает категории с _ в имени (например no_chaos).
    """
    prefix = "st_"
    raw = data[len(prefix):]  # убираем "st_"
    for key in sorted(CATEGORY_KEYS, key=len, reverse=True):
        if raw.startswith(key + "_"):
            status = raw[len(key) + 1:]
            return key, status
    return None, None


@router.callback_query(F.data == "fill_day")
async def fill_day(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    today = date.today().isoformat()
    entry = await get_or_create_entry(callback.from_user.id, today)
    summary = format_entry_summary(entry)
    await callback.message.edit_text(
        f"Заполни свой день ({today}):\n\n{summary}\n\nВыбери категорию:",
        reply_markup=categories_kb(entry),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cat_"))
async def choose_category(callback: CallbackQuery):
    category_key = callback.data.replace("cat_", "")
    await callback.message.edit_text(
        f"Как прошла категория?",
        reply_markup=status_kb(category_key),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("st_"))
async def set_status(callback: CallbackQuery):
    category_key, status = parse_status_callback(callback.data)
    if category_key is None:
        await callback.answer("Ошибка данных")
        return

    today = date.today().isoformat()
    user_id = callback.from_user.id

    await update_category(user_id, today, category_key, status)

    entry = await get_or_create_entry(user_id, today)
    score = calc_day_score(entry)
    await update_score(user_id, today, score)
    entry["day_score"] = score

    summary = format_entry_summary(entry)
    await callback.message.edit_text(
        f"Обновлено! Твой день ({today}):\n\n{summary}\n\nВыбери следующую категорию:",
        reply_markup=categories_kb(entry),
    )
    await callback.answer()


@router.callback_query(F.data == "add_note")
async def ask_note(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Напиши заметку к сегодняшнему дню (любой текст):"
    )
    await state.set_state(NoteState.waiting_for_note)
    await callback.answer()


@router.message(NoteState.waiting_for_note)
async def save_note(message: Message, state: FSMContext):
    today = date.today().isoformat()
    user_id = message.from_user.id
    await update_note(user_id, today, message.text)

    entry = await get_or_create_entry(user_id, today)
    summary = format_entry_summary(entry)
    await state.clear()
    await message.answer(
        f"Заметка сохранена!\n\n{summary}\n\nВыбери категорию или заверши день:",
        reply_markup=categories_kb(entry),
    )


@router.callback_query(F.data == "finish_day")
async def finish_day(callback: CallbackQuery):
    today = date.today().isoformat()
    user_id = callback.from_user.id
    entry = await get_or_create_entry(user_id, today)
    score = calc_day_score(entry)
    await update_score(user_id, today, score)

    summary = format_entry_summary(entry)
    recommendation = get_recommendation(entry)

    await callback.message.edit_text(
        f"День завершён!\n\n{summary}\n\n{recommendation}",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()
