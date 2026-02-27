from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

NEWS = [
    {
        'date': '23.02.2026',
        'title': '⚠️ Продление регистрации',
        'text': 'Теперь продлевать нужно за 10 дней!'
    },
    {
        'date': '22.02.2026',
        'title': '🏥 Медосмотр',
        'text': '1 марта бесплатный медосмотр'
    }
]

@router.message(Command('новости'))
@router.message(F.text == "📢 Новости")
async def show_news(message: Message):
    text = "📢 ПОСЛЕДНИЕ НОВОСТИ:\n\n"
    
    for news in NEWS:
        text += f"📅 {news['date']}\n"
        text += f"📌 {news['title']}\n"
        text += f"📝 {news['text']}\n\n"
    
    text += "👉 Подпишись на канал: @TurkmenStudentHub"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Перейти в канал", url="https://t.me/TurkmenStudentHub")]
    ])
    
    await message.answer(text, reply_markup=keyboard)