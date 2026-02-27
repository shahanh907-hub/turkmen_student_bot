from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import database as db

router = Router()

@router.message(Command('жильё'))
async def house_command(message: Message):
    if not message.from_user:
        return
    
    if not message.text:
        return
    
    text = message.text.replace('/жильё', '').strip()
    
    if not text:
        await message.answer(
            "❌ Напиши так:\n"
            "/жильё текст\n\n"
            "Пример: /жильё ищу комнату в Перми до 15000"
        )
        return
    
    contacts = f"@{message.from_user.username}" if message.from_user.username else f"id{message.from_user.id}"
    db.add_housing(message.from_user.id, text, contacts)
    
    await message.answer(
        f"✅ Объявление добавлено!\n\n"
        f"🏠 {text}\n"
        f"📞 Контакт: {contacts}"
    )

@router.message(Command('жильёвсе'))
async def housing_list(message: Message):
    items = db.get_all_housing()
    
    if not items:
        await message.answer("🏠 Пока нет объявлений")
        return
    
    text = "🏠 ЖИЛЬЁ:\n\n"
    for user_id, housing_text, contacts in items:
        user_info = db.get_user(user_id)
        username = f"@{user_info[0]}" if user_info and user_info[0] else f"id{user_id}"
        text += f"👤 {username}\n🏠 {housing_text}\n📞 {contacts}\n\n"
    
    await message.answer(text)