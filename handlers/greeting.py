from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message()
async def greeting_handler(message: Message):
    if not message.from_user:
        return
    
    if message.chat.type not in ['group', 'supergroup']:
        return
    
    if message.from_user.is_bot:
        return
    
    if not message.text:
        return
    
    text = message.text.lower()
    name = message.from_user.first_name or "друг"
    
    greetings = ['привет', 'салам', 'здравствуй', 'хай', 'hello', 'hi', 'привет бот', 'салам бот']
    
    if any(word in text for word in greetings):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🚫 ЧС", callback_data="group_chs"),
                InlineKeyboardButton(text="🚗 Поездки", callback_data="group_trips")
            ],
            [
                InlineKeyboardButton(text="🏠 Жильё", callback_data="group_housing"),
                InlineKeyboardButton(text="💰 Обмен", callback_data="group_exchange")
            ],
            [
                InlineKeyboardButton(text="📢 Канал", url="https://t.me/turkmen_student_perm")
            ]
        ])
        
        await message.reply(
            f"👋 Салам, {name}!\n\n"
            f"Нажми на кнопку, и я отвечу в личке 👇",
            reply_markup=keyboard
        )
        return