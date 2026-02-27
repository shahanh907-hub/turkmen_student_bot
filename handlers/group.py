from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(F.text.lower().in_([
    'привет бот', 'салам бот', 'salam bot', 'здравствуй бот',
    'привет', 'салам', 'здравствуй', 'хай', 'hello', 'hi'
]))
async def hello_bot(message: Message):
    if not message.from_user:
        return
    
    name = message.from_user.first_name or "друг"
    
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

@router.message(F.text.contains("@TurkmenStudentBot"))
async def mentioned_bot(message: Message):
    if not message.from_user:
        return
    
    name = message.from_user.first_name or "друг"
    
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

@router.message()
async def suggest_ads(message: Message):
    if message.chat.type not in ['group', 'supergroup']:
        return
    
    if not message.from_user or message.from_user.is_bot:
        return
    
    if not message.text:
        return
    
    text = message.text.lower()
    
    keywords = ['реклама', 'продаю', 'ищу', 'предлагаю', 'услуги', 'товар', 'продам', 'куплю']
    
    if any(word in text for word in keywords):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подать объявление", url="https://t.me/TurkmenStudentBot")]
        ])
        
        await message.reply(
            f"👋 Хочешь разместить рекламу?\n\n"
            f"У нас есть специальная доска объявлений!\n"
            f"Нажми на кнопку и добавь своё объявление 👇",
            reply_markup=keyboard
        )

@router.callback_query(F.data.startswith("group_"))
async def group_buttons(callback: CallbackQuery):
    if not callback or not callback.data or not callback.from_user or not callback.bot:
        await callback.answer("Ошибка")
        return
    
    try:
        action = callback.data.replace("group_", "")
        user_id = callback.from_user.id
        
        if action == "chs":
            await callback.bot.send_message(
                user_id,
                "🚫 ЧЁРНЫЙ СПИСОК\n\n"
                "Что хочешь сделать?\n\n"
                "• Чтобы посмотреть ЧС, нажми кнопку 🚫 ЧС в личке и выбери '📋 Посмотреть ЧС'\n"
                "• Чтобы добавить в ЧС, нажми кнопку 🚫 ЧС в личке и выбери '➕ Добавить в ЧС'"
            )
            await callback.answer("✅ Отправил в личку!")
            
        elif action == "trips":
            await callback.bot.send_message(
                user_id,
                "🚗 ПОЕЗДКИ И ПОПУТЧИКИ\n\n"
                "Что хочешь сделать?\n\n"
                "• Чтобы посмотреть все поездки, нажми кнопку 🚗 Поездки в личке и выбери '📋 Все поездки'\n"
                "• Чтобы добавить поездку, нажми кнопку 🚗 Поездки в личке и выбери '➕ Добавить поездку'"
            )
            await callback.answer("✅ Отправил в личку!")
            
        elif action == "housing":
            await callback.bot.send_message(
                user_id,
                "🏠 ЖИЛЬЁ\n\n"
                "Что хочешь сделать?\n\n"
                "• Чтобы посмотреть все объявления, нажми кнопку 🏠 Жильё в личке и выбери '📋 Все объявления'\n"
                "• Чтобы добавить объявление, нажми кнопку 🏠 Жильё в личке и выбери '➕ Добавить жильё'"
            )
            await callback.answer("✅ Отправил в личку!")
            
        elif action == "exchange":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💰 Перейти к обмену", url="https://t.me/TurkmenStudentBot")]
            ])
            
            await callback.bot.send_message(
                user_id,
                "💰 ОБМЕН ВАЛЮТ\n\n"
                "В личном кабинете бота ты можешь:\n"
                "• Посмотреть белый список обменников\n"
                "• Посмотреть чёрный список\n"
                "• Добавить новый обменник\n"
                "• Оставить отзыв\n\n"
                "Нажми на кнопку ниже 👇",
                reply_markup=keyboard
            )
            await callback.answer("✅ Отправил в личку!")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        await callback.answer("❌ Ошибка")