from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command('help'))
async def help_command(message: Message):
    """Общая помощь"""
    await message.answer(
        "📌 **ДОСТУПНЫЕ КОМАНДЫ:**\n\n"
        "🚫 **ЧС:**\n"
        "  /chs добавить @ник причина\n"
        "  /chs список\n"
        "  /check @ник\n\n"
        "🚗 **Поездки:**\n"
        "  /trip добавить текст\n"
        "  /trips\n\n"
        "🏠 **Жильё:**\n"
        "  /house добавить текст\n"
        "  /housing\n\n"
        "🏢 **Организации:**\n"
        "  /org\n\n"
        "📢 **Новости:**\n"
        "  /news"
    )