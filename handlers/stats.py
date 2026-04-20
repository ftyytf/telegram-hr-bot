from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import date, timedelta

from database import get_or_create_entry, get_entries_for_period
from keyboards import main_menu_kb
from services import format_entry_summary, get_recommendation, calc_day_score

router = Router()


@router.callback_query(F.data == "show_day")
async def show_today(callback: CallbackQuery):
    today = date.today().isoformat()
    entry = await get_or_create_entry(callback.from_user.id, today)
    summary = format_entry_summary(entry)
    await callback.message.edit_text(
        f"Твой день ({today}):\n\n{summary}",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "recommend")
async def show_recommendation(callback: CallbackQuery):
    today = date.today().isoformat()
    entry = await get_or_create_entry(callback.from_user.id, today)
    recommendation = get_recommendation(entry)
    await callback.message.edit_text(
        f"Рекомендация на основе сегодняшнего дня:\n\n{recommendation}",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "stats_week")
async def stats_week(callback: CallbackQuery):
    today = date.today()
    week_ago = today - timedelta(days=6)
    entries = await get_entries_for_period(
        callback.from_user.id,
        week_ago.isoformat(),
        today.isoformat(),
    )

    if not entries:
        await callback.message.edit_text(
            "За последнюю неделю записей нет. Начни заполнять день!",
            reply_markup=main_menu_kb(),
        )
        await callback.answer()
        return

    total_score = 0
    days_count = len(entries)
    lines = []

    for e in entries:
        score = calc_day_score(e)
        total_score += score
        lines.append(f'{e["entry_date"]}: {score}/14')

    avg = round(total_score / days_count, 1)

    text = (
        f"Статистика за {days_count} дн. "
        f"({week_ago.isoformat()} - {today.isoformat()}):\n\n"
        + "\n".join(lines)
        + f"\n\nСредний балл: {avg}/14"
        + f"\nВсего баллов: {total_score}"
    )

    if avg >= 10:
        text += "\n\nОтличная неделя! Держи темп!"
    elif avg >= 6:
        text += "\n\nНеплохая неделя. Есть куда расти!"
    else:
        text += "\n\nСлабая неделя. Но ты отслеживаешь - это уже шаг вперёд!"

    await callback.message.edit_text(text, reply_markup=main_menu_kb())
    await callback.answer()
