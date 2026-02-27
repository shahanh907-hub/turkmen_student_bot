from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

import database as db

router = Router()

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚫 ЧС"), KeyboardButton(text="✅ Проверить")],
            [KeyboardButton(text="🚗 Поездки"), KeyboardButton(text="🏠 Жильё")],
            [KeyboardButton(text="💰 Обмен валют"), KeyboardButton(text="📢 Объявления")],
            [KeyboardButton(text="🏢 Организации"), KeyboardButton(text="📢 Канал")],
            [KeyboardButton(text="❓ Помощь")]
        ],
        resize_keyboard=True
    )

@router.message(Command('start'))
async def cmd_start(message: Message):
    if not message.from_user:
        return
    
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or "User"
    
    db.add_user(user_id, username, first_name)
    
    await message.answer(
        f"👋 Привет, {first_name}!\n\n"
        f"🇹🇲 Я бот-помощник туркменских студентов\n\n"
        f"📌 Что я умею:\n"
        f"• 🚫 Добавлять мошенников в ЧС\n"
        f"• ✅ Проверять людей\n"
        f"• 🚗 Искать попутчиков\n"
        f"• 🏠 Находить жильё\n"
        f"• 💰 Безопасный обмен валют\n"
        f"• 📢 Доска объявлений\n"
        f"• 🏢 Давать контакты организаций\n"
        f"• 📢 Канал с новостями\n\n"
        f"👇 Нажимай на кнопки внизу!",
        reply_markup=main_keyboard()
    )