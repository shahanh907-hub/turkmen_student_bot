from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from collections import defaultdict

router = Router()

user_warnings = defaultdict(int)
is_moderation_active = True

MAX_MESSAGES = 10
WARNING_LIMIT = 3

@router.message()
async def check_messages(message: Message):
    if not message.from_user:
        return
    
    if message.chat.type not in ['group', 'supergroup']:
        return
    
    if message.from_user.is_bot:
        return
    
    if not is_moderation_active:
        return
    
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "пользователь"
    
    user_warnings[user_id] += 1
    warning_count = user_warnings[user_id]
    
    if warning_count >= MAX_MESSAGES and warning_count <= WARNING_LIMIT:
        await message.answer(
            f"⚠️ Внимание, {user_name}!\n"
            f"Это предупреждение {warning_count} из {WARNING_LIMIT}."
        )