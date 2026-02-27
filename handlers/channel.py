from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

CHANNEL_USERNAME = "@turkmen_student_perm"

@router.message(Command('канал'))
async def cmd_channel(message: Message):
    if not message.from_user:
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")]
    ])
    
    await message.answer(
        f"📢 НАШ КАНАЛ\n\n"
        f"{CHANNEL_USERNAME}\n\n"
        f"🔹 Новости вузов\n"
        f"🔹 Изменения в законах\n"
        f"🔹 Проверенные контакты\n"
        f"🔹 Скидки для студентов\n"
        f"🔹 Рекламные объявления\n\n"
        f"Подписывайся! 👇",
        reply_markup=keyboard
    )