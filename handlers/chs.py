from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import database as db

router = Router()

@router.message(Command('чс'))
async def chs_command(message: Message):
    if not message.from_user or not message.text:
        return
    
    parts = message.text.split(maxsplit=2)
    
    if len(parts) < 2:
        await message.answer(
            "❌ Как использовать:\n\n"
            "/чс добавить @ник причина - добавить в ЧС\n"
            "/чс список - посмотреть ЧС\n\n"
            "Пример: /чс добавить @badman кинул на 5000 рублей"
        )
        return
    
    action = parts[1].lower()
    
    if action == "добавить":
        if len(parts) < 3:
            await message.answer("❌ Напиши: /чс добавить @ник причина")
            return
        
        rest = parts[2].split(maxsplit=1)
        if len(rest) < 1:
            await message.answer("❌ Укажи @ник")
            return
        
        tg_login = rest[0].replace('@', '')
        reason = rest[1] if len(rest) > 1 else "без причины"
        
        db.add_to_blacklist(tg_login, reason, message.from_user.id)
        
        await message.answer(
            f"✅ Добавлено в ЧС!\n\n"
            f"👤 @{tg_login}\n"
            f"📝 Причина: {reason}"
        )
    
    elif action == "список":
        items = db.get_recent_blacklist()
        
        if items:
            text = "🚫 ЧЁРНЫЙ СПИСОК:\n\n"
            for tg, reason in items:
                text += f"• @{tg} — {reason}\n"
        else:
            text = "🚫 ЧС пока пуст"
        
        await message.answer(text)
    
    else:
        await message.answer("❌ Используй: /чс добавить или /чс список")

@router.message(Command('check'))
async def check_command(message: Message):
    if not message.text:
        return
    
    parts = message.text.split()
    
    if len(parts) < 2:
        await message.answer("❌ Напиши: /check @ник\n\nПример: /check @durov")
        return
    
    tg_login = parts[1].replace('@', '')
    result = db.check_user_in_blacklist(tg_login)
    
    if result and result[0] > 0:
        count = result[0]
        reasons = result[1] if result[1] else "нет описания"
        await message.answer(
            f"⚠️ На @{tg_login} {count} жалоб!\n"
            f"📋 Причины: {reasons}"
        )
    else:
        await message.answer(f"✅ @{tg_login} чист")