from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import date, timedelta

from database import get_or_create_entry, get_entries_for_period
from keyboards import main_menu_kb
from services import format_entry_summary, get_recommendation, calc_day_score
from utils.formatting import today_card, recommendation_card, week_stats_card

router = Router()


@router.callback_query(F.data == "show_day")
async def show_today(callback: CallbackQuery):
    today = date.today().isoformat()
    entry = await get_or_create_entry(callback.from_user.id, today)
    score = calc_day_score(entry)
    summary = format_entry_summary(entry)
    await callback.message.edit_text(
        today_card(today, summary, score),
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "recommend")
async def show_recommendation(callback: CallbackQuery):
    today = date.today().isoformat()
    entry = await get_or_create_entry(callback.from_user.id, today)
    recommendation = get_recommendation(entry)
    await callback.message.edit_text(
        recommendation_card(recommendation),
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
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
            "┌─────────────────────────┐\n"
            "   📊 <b>Статистика</b>\n"
            "├─────────────────────────┤\n"
            "   За неделю записей нет.\n"
            "   Начни заполнять день! 💪\n"
            "└─────────────────────────┘",
            reply_markup=main_menu_kb(),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    days_data = []
    for e in entries:
        score = calc_day_score(e)
        days_data.append((e["entry_date"], score))

    await callback.message.edit_text(
        week_stats_card(week_ago.isoformat(), today.isoformat(), days_data),
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )
    await callback.answer()
