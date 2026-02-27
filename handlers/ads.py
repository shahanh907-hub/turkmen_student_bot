from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import sqlite3
import datetime

router = Router()

class AdsStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_type = State()

def init_ads_db():
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        ad_text TEXT,
        ad_type TEXT,
        created_date TEXT,
        views INTEGER DEFAULT 0
    )
    ''')
    conn.commit()
    conn.close()

init_ads_db()

@router.message(F.text == "📢 Объявления")
async def ads_menu(message: Message):
    if message.chat.type != 'private':
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Все объявления", callback_data="ads_all")],
        [InlineKeyboardButton(text="➕ Подать объявление", callback_data="ads_add")],
        [InlineKeyboardButton(text="📊 Мои объявления", callback_data="ads_my")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ])
    
    await message.answer(
        "📢 ДОСКА ОБЪЯВЛЕНИЙ\n\n"
        "Что хочешь сделать?\n"
        "• 📋 Посмотреть все объявления\n"
        "• ➕ Подать своё объявление\n"
        "• 📊 Мои объявления",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "ads_all")
async def ads_all(callback: CallbackQuery):
    if not callback.message:
        await callback.answer()
        return
    
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('SELECT username, ad_text, created_date FROM ads ORDER BY id DESC LIMIT 10')
    ads = cur.fetchall()
    conn.close()
    
    if not ads:
        await callback.message.answer(
            "📢 Пока нет объявлений.\n\n"
            "Нажми '➕ Подать объявление' чтобы быть первым!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="➕ Подать объявление", callback_data="ads_add")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="ads_menu")]
            ])
        )
        await callback.answer()
        return
    
    text = "📢 ВСЕ ОБЪЯВЛЕНИЯ:\n\n"
    for username, ad_text, created_date in ads:
        date_str = created_date[:10] if created_date else ""
        text += f"👤 {username}\n📝 {ad_text}\n📅 {date_str}\n\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Подать объявление", callback_data="ads_add")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="ads_menu")]
    ])
    
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "ads_add")
async def ads_add_start(callback: CallbackQuery, state: FSMContext):
    if not callback.message:
        await callback.answer()
        return
    
    await state.set_state(AdsStates.waiting_for_text)
    
    await callback.message.answer(
        "📢 НОВОЕ ОБЪЯВЛЕНИЕ\n\n"
        "Напиши текст объявления в одном сообщении.\n\n"
        "Например:\n"
        "Продаю iPhone 12, состояние идеальное, 40000 руб\n\n"
        "Или отправь /cancel",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="ads_menu")]
        ])
    )
    await callback.answer()

@router.message(AdsStates.waiting_for_text)
async def ads_get_text(message: Message, state: FSMContext):
    if not message.text:
        return
    
    await state.update_data(ad_text=message.text)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💼 Товар/Услуга", callback_data="ads_type_product")],
        [InlineKeyboardButton(text="🔍 Ищу/Предлагаю", callback_data="ads_type_search")],
        [InlineKeyboardButton(text="🎉 Событие", callback_data="ads_type_event")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="ads_menu")]
    ])
    
    await message.answer(
        "📢 Выбери тип объявления:",
        reply_markup=keyboard
    )
    await state.set_state(AdsStates.waiting_for_type)

@router.callback_query(AdsStates.waiting_for_type)
async def ads_get_type(callback: CallbackQuery, state: FSMContext):
    if not callback.data or not callback.message:
        return
    
    ad_type = callback.data.replace("ads_type_", "")
    data = await state.get_data()
    ad_text = data.get('ad_text')
    
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO ads (user_id, username, ad_text, ad_type, created_date)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        callback.from_user.id,
        f"@{callback.from_user.username}" if callback.from_user.username else f"id{callback.from_user.id}",
        ad_text,
        ad_type,
        datetime.datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    
    await state.clear()
    
    await callback.message.answer(
        "✅ Объявление добавлено!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📋 Все объявления", callback_data="ads_all")],
            [InlineKeyboardButton(text="➕ Ещё объявление", callback_data="ads_add")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="ads_menu")]
        ])
    )
    await callback.answer()

@router.callback_query(F.data == "ads_my")
async def ads_my(callback: CallbackQuery):
    if not callback.message or not callback.from_user:
        await callback.answer()
        return
    
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('SELECT ad_text, created_date, views FROM ads WHERE user_id = ? ORDER BY id DESC', 
                (callback.from_user.id,))
    ads = cur.fetchall()
    conn.close()
    
    if not ads:
        await callback.message.answer(
            "📢 У тебя пока нет объявлений.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="➕ Подать объявление", callback_data="ads_add")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="ads_menu")]
            ])
        )
        await callback.answer()
        return
    
    text = "📢 МОИ ОБЪЯВЛЕНИЯ:\n\n"
    for ad_text, created_date, views in ads:
        date_str = created_date[:10] if created_date else ""
        text += f"📝 {ad_text}\n📅 {date_str}  👁 {views}\n\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Новое объявление", callback_data="ads_add")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="ads_menu")]
    ])
    
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()

@router.message(Command('cancel'))
async def cancel_ads(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Отменено")

@router.callback_query(F.data == "ads_menu")
async def back_to_ads_menu(callback: CallbackQuery):
    if not callback.message:
        await callback.answer()
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Все объявления", callback_data="ads_all")],
        [InlineKeyboardButton(text="➕ Подать объявление", callback_data="ads_add")],
        [InlineKeyboardButton(text="📊 Мои объявления", callback_data="ads_my")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ])
    
    await callback.message.answer(
        "📢 ДОСКА ОБЪЯВЛЕНИЙ\n\n"
        "Что хочешь сделать?\n"
        "• 📋 Посмотреть все объявления\n"
        "• ➕ Подать своё объявление\n"
        "• 📊 Мои объявления",
        reply_markup=keyboard
    )
    await callback.answer()