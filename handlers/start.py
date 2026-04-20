from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from database import add_user
from keyboards import main_menu_kb
from utils.formatting import welcome_card

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or "",
    )
    name = message.from_user.first_name or "друг"
    await message.answer(
        welcome_card(name),
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "back_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "╔══════════════════════════╗\n"
        "   🏠 <b>Главное меню</b>\n"
        "╠══════════════════════════╣\n"
        "   Выбери действие:\n"
        "╚══════════════════════════╝",
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )
    await callback.answer()
