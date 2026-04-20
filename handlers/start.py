from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from database import add_user
from keyboards import main_menu_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or "",
    )
    await message.answer(
        "Привет! Я твой трекер дня.\n\n"
        "Каждый день отмечай 7 ключевых сфер жизни,\n"
        "получай рекомендации и следи за прогрессом.",
        reply_markup=main_menu_kb(),
    )


@router.callback_query(F.data == "back_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Главное меню. Выбери действие:",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()
