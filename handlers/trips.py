from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import database as db

router = Router()

@router.message(Command('поездка'))
async def trip_command(message: Message):
    if not message.from_user:
        return
    
    if not message.text:
        return
    
    text = message.text.replace('/поездка', '').strip()
    
    if not text:
        await message.answer(
            "❌ Напиши так:\n"
            "/поездка текст\n\n"
            "Пример: /поездка завтра в Казань"
        )
        return
    
    contacts = f"@{message.from_user.username}" if message.from_user.username else f"id{message.from_user.id}"
    db.add_trip(message.from_user.id, text, contacts)
    
    await message.answer(
        f"✅ Поездка добавлена!\n\n"
        f"📝 {text}\n"
        f"📞 Контакт: {contacts}"
    )

@router.message(Command('поездки'))
async def trips_list(message: Message):
    trips = db.get_all_trips()
    
    if not trips:
        await message.answer("🚗 Пока нет поездок")
        return
    
    text = "🚗 ПОЕЗДКИ:\n\n"
    for user_id, trip_text, contacts in trips:
        user_info = db.get_user(user_id)
        username = f"@{user_info[0]}" if user_info and user_info[0] else f"id{user_id}"
        text += f"👤 {username}\n📝 {trip_text}\n📞 {contacts}\n\n"
    
    await message.answer(text)