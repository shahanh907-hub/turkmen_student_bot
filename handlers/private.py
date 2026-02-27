from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database as db

router = Router()

# Состояния для ЧС
class ChsStates(StatesGroup):
    waiting_for_nick = State()
    waiting_for_reason = State()

# Состояния для поездок
class TripStates(StatesGroup):
    waiting_for_text = State()

# Состояния для жилья
class HousingStates(StatesGroup):
    waiting_for_text = State()

# Состояния для проверки
class CheckStates(StatesGroup):
    waiting_for_nick = State()

# Состояния для обмена валют
class ExchangeStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_contact = State()
    waiting_for_rates = State()
    waiting_for_city = State()
    waiting_for_rating = State()
    waiting_for_review = State()
    waiting_for_review_text = State()

def private_keyboard():
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
async def private_start(message: Message):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    first_name = message.from_user.first_name or "User"
    
    db.add_user(message.from_user.id, message.from_user.username, first_name)
    
    await message.answer(
        f"👋 Привет, {first_name}!\n\n"
        f"🇹🇲 Твой личный кабинет\n\n"
        f"📌 Что я умею:\n"
        f"• 🚫 Добавлять мошенников в ЧС\n"
        f"• ✅ Проверять людей\n"
        f"• 🚗 Искать попутчиков\n"
        f"• 🏠 Находить жильё\n"
        f"• 💰 Безопасный обмен валют\n"
        f"• 📢 Доска объявлений\n"
        f"• 🏢 Давать контакты организаций\n"
        f"• 📢 Новости и канал\n\n"
        f"👇 Нажимай на кнопки внизу!",
        reply_markup=private_keyboard()
    )

@router.message(F.text == "🚫 ЧС")
async def private_chs(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Посмотреть ЧС")],
            [KeyboardButton(text="➕ Добавить в ЧС")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "🚫 ЧЁРНЫЙ СПИСОК\n\n"
        "Что хочешь сделать?",
        reply_markup=keyboard
    )

@router.message(F.text == "➕ Добавить в ЧС")
async def add_chs_start(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    await state.set_state(ChsStates.waiting_for_nick)
    await message.answer(
        "👤 Введи ник мошенника:\n\n"
        "Например: @badman\n\n"
        "Или нажми ❌ Отмена",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="❌ Отмена")]],
            resize_keyboard=True
        )
    )

@router.message(ChsStates.waiting_for_nick)
async def process_nick(message: Message, state: FSMContext):
    if not message.from_user or not message.text:
        return
    
    if message.text == "❌ Отмена":
        await state.clear()
        await private_chs(message, state)
        return
    
    nick = message.text.replace('@', '').strip()
    if not nick:
        await message.answer("❌ Напиши никнейм")
        return
    
    await state.update_data(nick=nick)
    await state.set_state(ChsStates.waiting_for_reason)
    
    await message.answer(
        "📝 Введи причину:\n\n"
        "Например: кинул на 5000 рублей, не отдал долг\n\n"
        "Или нажми ❌ Отмена"
    )

@router.message(ChsStates.waiting_for_reason)
async def process_reason(message: Message, state: FSMContext):
    if not message.from_user or not message.text:
        return
    
    if message.text == "❌ Отмена":
        await state.clear()
        await private_chs(message, state)
        return
    
    reason = message.text.strip()
    if not reason:
        await message.answer("❌ Напиши причину")
        return
    
    data = await state.get_data()
    nick = data.get('nick')
    
    db.add_to_blacklist(nick, reason, message.from_user.id)
    
    await state.clear()
    
    await message.answer(
        f"✅ Добавлено в ЧС!\n\n"
        f"👤 @{nick}\n"
        f"📝 Причина: {reason}",
        reply_markup=private_keyboard()
    )

@router.message(F.text == "📋 Посмотреть ЧС")
async def view_chs(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    items = db.get_recent_blacklist()
    
    if items:
        text = "🚫 ЧЁРНЫЙ СПИСОК:\n\n"
        for tg, reason in items:
            text += f"• @{tg} — {reason}\n"
    else:
        text = "🚫 ЧС пока пуст.\n\nНажми '➕ Добавить в ЧС' чтобы добавить первого!"
    
    await message.answer(text, reply_markup=private_keyboard())

@router.message(F.text == "✅ Проверить")
async def private_check(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    await state.set_state(CheckStates.waiting_for_nick)
    await message.answer(
        "🔍 Введи никнейм человека, которого хочешь проверить:\n\n"
        "Например: @durov\n\n"
        "Или нажми ❌ Отмена",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="❌ Отмена")]],
            resize_keyboard=True
        )
    )

@router.message(CheckStates.waiting_for_nick)
async def process_check_nick(message: Message, state: FSMContext):
    if not message.from_user or not message.text:
        return
    
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer(
            "👋 Проверка отменена",
            reply_markup=private_keyboard()
        )
        return
    
    nick = message.text.replace('@', '').strip()
    if not nick:
        await message.answer("❌ Напиши никнейм")
        return
    
    result = db.check_user_in_blacklist(nick)
    
    await state.clear()
    
    if result and result[0] > 0:
        count = result[0]
        reasons = result[1] if result[1] else "нет описания"
        await message.answer(
            f"⚠️ На @{nick} {count} жалоб!\n"
            f"📋 Причины: {reasons}",
            reply_markup=private_keyboard()
        )
    else:
        await message.answer(
            f"✅ @{nick} чист. Жалоб нет.",
            reply_markup=private_keyboard()
        )

@router.message(F.text == "🚗 Поездки")
async def private_trips(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Все поездки")],
            [KeyboardButton(text="➕ Добавить поездку")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "🚗 ПОЕЗДКИ И ПОПУТЧИКИ\n\n"
        "Что хочешь сделать?",
        reply_markup=keyboard
    )

@router.message(F.text == "➕ Добавить поездку")
async def add_trip_start(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    await state.set_state(TripStates.waiting_for_text)
    await message.answer(
        "📝 Напиши информацию о поездке:\n\n"
        "Например: завтра еду в Казань, есть 2 места\n"
        "Или: 28 февраля ищу попутчика в Москву\n\n"
        "Или нажми ❌ Отмена",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="❌ Отмена")]],
            resize_keyboard=True
        )
    )

@router.message(TripStates.waiting_for_text)
async def process_trip_text(message: Message, state: FSMContext):
    if not message.from_user or not message.text:
        return
    
    if message.text == "❌ Отмена":
        await state.clear()
        await private_trips(message, state)
        return
    
    trip_text = message.text.strip()
    if not trip_text:
        await message.answer("❌ Напиши информацию о поездке")
        return
    
    contacts = f"@{message.from_user.username}" if message.from_user.username else f"id{message.from_user.id}"
    
    db.add_trip(message.from_user.id, trip_text, contacts)
    
    await state.clear()
    
    await message.answer(
        f"✅ Поездка добавлена!\n\n"
        f"📝 {trip_text}\n"
        f"📞 Контакт: {contacts}",
        reply_markup=private_keyboard()
    )

@router.message(F.text == "📋 Все поездки")
async def view_trips(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    trips = db.get_all_trips()
    
    if not trips:
        await message.answer("🚗 Пока нет поездок")
        return
    
    text = "🚗 ВСЕ ПОЕЗДКИ:\n\n"
    for user_id, trip_text, contacts in trips:
        user_info = db.get_user(user_id)
        username = f"@{user_info[0]}" if user_info and user_info[0] else f"id{user_id}"
        text += f"👤 {username}\n📝 {trip_text}\n📞 {contacts}\n\n"
    
    await message.answer(text, reply_markup=private_keyboard())

@router.message(F.text == "🏠 Жильё")
async def private_housing(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Все объявления")],
            [KeyboardButton(text="➕ Добавить жильё")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "🏠 ЖИЛЬЁ\n\n"
        "Что хочешь сделать?",
        reply_markup=keyboard
    )

@router.message(F.text == "➕ Добавить жильё")
async def add_housing_start(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    await state.set_state(HousingStates.waiting_for_text)
    await message.answer(
        "📝 Напиши информацию о жильё:\n\n"
        "Например: ищу комнату в Перми до 15000 рублей\n"
        "Или: сдаю квартиру в Казани 20000 рублей, 2 комнаты\n\n"
        "Или нажми ❌ Отмена",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="❌ Отмена")]],
            resize_keyboard=True
        )
    )

@router.message(HousingStates.waiting_for_text)
async def process_housing_text(message: Message, state: FSMContext):
    if not message.from_user or not message.text:
        return
    
    if message.text == "❌ Отмена":
        await state.clear()
        await private_housing(message, state)
        return
    
    housing_text = message.text.strip()
    if not housing_text:
        await message.answer("❌ Напиши информацию о жильё")
        return
    
    contacts = f"@{message.from_user.username}" if message.from_user.username else f"id{message.from_user.id}"
    
    db.add_housing(message.from_user.id, housing_text, contacts)
    
    await state.clear()
    
    await message.answer(
        f"✅ Объявление добавлено!\n\n"
        f"🏠 {housing_text}\n"
        f"📞 Контакт: {contacts}",
        reply_markup=private_keyboard()
    )

@router.message(F.text == "📋 Все объявления")
async def view_housing(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    items = db.get_all_housing()
    
    if not items:
        await message.answer("🏠 Пока нет объявлений")
        return
    
    text = "🏠 ВСЕ ОБЪЯВЛЕНИЯ:\n\n"
    for user_id, housing_text, contacts in items:
        user_info = db.get_user(user_id)
        username = f"@{user_info[0]}" if user_info and user_info[0] else f"id{user_id}"
        text += f"👤 {username}\n🏠 {housing_text}\n📞 {contacts}\n\n"
    
    await message.answer(text, reply_markup=private_keyboard())

@router.message(F.text == "💰 Обмен валют")
async def private_exchange(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Белый список")],
            [KeyboardButton(text="🚫 Чёрный список обменников")],
            [KeyboardButton(text="➕ Добавить обменник")],
            [KeyboardButton(text="⭐ Оценить обменник")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "💰 ОБМЕН ВАЛЮТ\n\n"
        "Что хочешь сделать?\n"
        "• 📋 Белый список - проверенные обменники\n"
        "• 🚫 Чёрный список - мошенники\n"
        "• ➕ Добавить обменник - если знаешь надёжный\n"
        "• ⭐ Оценить обменник - поделись опытом",
        reply_markup=keyboard
    )

@router.message(F.text == "📋 Белый список")
async def white_list(message: Message):
    if message.chat.type != 'private':
        return
    
    items = db.get_all_exchangers()
    
    if not items:
        await message.answer(
            "📋 Белый список пока пуст.\n\n"
            "Нажми '➕ Добавить обменник' чтобы добавить первый!",
            reply_markup=private_keyboard()
        )
        return
    
    text = "✅ БЕЛЫЙ СПИСОК ОБМЕННИКОВ:\n\n"
    for id, name, city, contact, rates, rating, reviews in items:
        stars = "⭐" * int(rating) if rating else "⭐"
        text += f"• {name}\n"
        text += f"  📍 {city}\n"
        text += f"  📞 {contact}\n"
        text += f"  💱 {rates}\n"
        text += f"  {stars} ({reviews} отзывов)\n\n"
    
    await message.answer(text, reply_markup=private_keyboard())

@router.message(F.text == "🚫 Чёрный список обменников")
async def black_list(message: Message):
    if message.chat.type != 'private':
        return
    
    items = db.get_scam_exchangers()
    
    if not items:
        await message.answer(
            "🚫 Чёрный список обменников пока пуст.",
            reply_markup=private_keyboard()
        )
        return
    
    text = "🚫 ЧЁРНЫЙ СПИСОК ОБМЕННИКОВ:\n\n"
    for name, contact, reason in items:
        text += f"• {name}\n"
        text += f"  📞 {contact}\n"
        text += f"  ⚠️ {reason}\n\n"
    
    await message.answer(text, reply_markup=private_keyboard())

@router.message(F.text == "🏢 Организации")
async def private_org(message: Message):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    from .organizations import show_org_menu
    await show_org_menu(message)

@router.message(F.text == "📢 Объявления")
async def private_ads(message: Message):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    from .ads import ads_menu
    await ads_menu(message)

@router.message(F.text == "📢 Канал")
async def private_channel(message: Message):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    CHANNEL_USERNAME = "@turkmen_student_perm"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Перейти в канал", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")]
    ])
    
    await message.answer(
        f"📢 НАШ КАНАЛ\n\n"
        f"{CHANNEL_USERNAME}\n\n"
        f"🔹 Новости вузов\n"
        f"🔹 Изменения в законах\n"
        f"🔹 Проверенные контакты\n"
        f"🔹 Скидки для студентов\n"
        f"🔹 Рекламные объявления\n\n"
        f"👇 Подписывайся, чтобы ничего не пропустить!",
        reply_markup=keyboard
    )

@router.message(F.text == "❓ Помощь")
async def private_help(message: Message):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    await message.answer(
        "📌 КАК ПОЛЬЗОВАТЬСЯ БОТОМ:\n\n"
        "🚫 ЧЁРНЫЙ СПИСОК\n"
        "• Нажми кнопку 🚫 ЧС\n"
        "• Выбери ➕ Добавить в ЧС\n"
        "• Введи ник и причину\n\n"
        
        "✅ ПРОВЕРКА\n"
        "• Нажми кнопку ✅ Проверить\n"
        "• Введи никнейм человека\n"
        "• Бот покажет, есть ли на него жалобы\n\n"
        
        "🚗 ПОЕЗДКИ\n"
        "• Нажми кнопку 🚗 Поездки\n"
        "• Выбери ➕ Добавить поездку\n"
        "• Напиши куда и когда едешь\n\n"
        
        "🏠 ЖИЛЬЁ\n"
        "• Нажми кнопку 🏠 Жильё\n"
        "• Выбери ➕ Добавить жильё\n"
        "• Напиши что ищешь или сдаёшь\n\n"
        
        "💰 ОБМЕН ВАЛЮТ\n"
        "• Нажми кнопку 💰 Обмен валют\n"
        "• Смотри белый и чёрный списки\n\n"
        
        "📢 ОБЪЯВЛЕНИЯ\n"
        "• Нажми кнопку 📢 Объявления\n"
        "• Смотри все объявления\n"
        "• Добавляй свои\n\n"
        
        "🏢 ОРГАНИЗАЦИИ\n"
        "• Нажми кнопку 🏢 Организации\n"
        "• МФЦ, страховка, медкнижка, фитнес\n\n"
        
        "📢 КАНАЛ\n"
        "• Нажми кнопку 📢 Канал\n"
        "• Перейди в канал и подпишись\n\n"
        
        "❓ Если что-то непонятно - просто нажимай на кнопки!\n"
        "Бот сам подскажет что делать 👌",
        reply_markup=private_keyboard()
    )

@router.message(F.text == "🔙 Назад")
async def go_back(message: Message, state: FSMContext):
    if message.chat.type != 'private':
        return
    
    if not message.from_user:
        return
    
    await state.clear()
    await message.answer(
        "👋 Главное меню",
        reply_markup=private_keyboard()
    )