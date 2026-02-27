from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import sqlite3
import datetime
from typing import Optional

router = Router()

CHANNEL_ID = -1001234567890  # Узнай через @getidsbot

KEYWORDS = [
    'продаю', 'продам', 'куплю', 'ищу', 'сдаю', 'сниму',
    'услуги', 'предлагаю', 'реклама', 'товар', 'скидка',
    'помощь', 'работа', 'вакансия', 'требуется'
]

def is_advertisement(text: str) -> bool:
    if not text:
        return False
    
    text_lower = text.lower()
    for word in KEYWORDS:
        if word in text_lower:
            return True
    return False

def save_ad_to_db(user_id: int, username: str, text: str):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS reposted_ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        ad_text TEXT,
        reposted_date TEXT,
        status TEXT DEFAULT 'новое'
    )
    ''')
    cur.execute('''
    INSERT INTO reposted_ads (user_id, username, ad_text, reposted_date)
    VALUES (?, ?, ?, ?)
    ''', (user_id, username, text, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

async def send_to_channel(bot, user_name: str, ad_text: str, original_message: Optional[Message] = None):
    channel_text = (
        f"📢 Рекламное объявление\n\n"
        f"{ad_text}\n\n"
        f"👤 Автор: {user_name}\n"
        f"📅 {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )
    
    keyboard = None
    if original_message and original_message.from_user and original_message.from_user.username:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="👤 Связаться с автором", 
                url=f"https://t.me/{original_message.from_user.username}"
            )]
        ])
    
    try:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=channel_text,
            reply_markup=keyboard
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки в канал: {e}")
        return False

@router.message()
async def check_and_repost(message: Message):
    if not message.from_user:
        return
    
    if message.chat.type not in ['group', 'supergroup']:
        return
    
    if message.from_user.is_bot:
        return
    
    if not message.text:
        return
    
    if not is_advertisement(message.text):
        return
    
    user_name = message.from_user.first_name or "пользователь"
    if message.from_user.username:
        user_display = f"@{message.from_user.username} ({user_name})"
    else:
        user_display = user_name
    
    # Явно передаем message, который точно не None
    success = await send_to_channel(
        message.bot, 
        user_display, 
        message.text,
        message
    )
    
    if success:
        save_ad_to_db(
            message.from_user.id,
            message.from_user.username or "без username",
            message.text
        )
        
        await message.reply(
            f"✅ Ваше объявление отправлено в канал!\n\n"
            f"Оно появится в @turkmen_student_perm"
        )
    else:
        await message.reply(
            f"❌ Не удалось отправить объявление в канал.\n"
            f"Попробуйте позже или напишите в личку боту."
        )