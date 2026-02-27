from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

ORGANIZATIONS = {
    'mfc_1': {
        'name': 'МФЦ Перми (Космонавтов)',
        'address': 'шоссе Космонавтов, 65 • этаж 3',
        'phone': '+7 (342) 270-11-20',
        'hours': 'Пн-Пт 9:00-20:00, Сб 9:00-17:00',
        'services': 'Паспорт, регистрация, ИНН, СНИЛС',
        'site': 'mfc.permkrai.ru'
    },
    'mfc_2': {
        'name': 'МФЦ Перми (Попова)',
        'address': 'улица Попова, 23 • этаж 2',
        'phone': '8 (800) 234-32-75',
        'hours': 'Пн-Пт 9:00-20:00, Сб 9:00-17:00',
        'services': 'Паспорт, регистрация, ИНН, СНИЛС',
        'site': 'mfc.permkrai.ru'
    },
    'mfc_3': {
        'name': 'МФЦ Перми (Куйбышева)',
        'address': 'улица Куйбышева, 9',
        'phone': '8 (800) 234-32-75',
        'hours': 'Пн-Пт 9:00-20:00, Сб 9:00-17:00',
        'services': 'Паспорт, регистрация, ИНН, СНИЛС',
        'site': 'mfc.permkrai.ru'
    },
    'mfc_4': {
        'name': 'МФЦ Перми (Ленина)',
        'address': 'улица Ленина, 92 • офис 100, этаж 1',
        'phone': '8 (800) 234-32-75',
        'hours': 'Пн-Пт 9:00-20:00, Сб 9:00-17:00',
        'services': 'Паспорт, регистрация, ИНН, СНИЛС',
        'site': 'mfc.permkrai.ru'
    },
    'insurance_malkysha': {
        'name': 'Страхование (Малькиша)',
        'address': 'Комсомольский проспект, 84',
        'phone': '+7 995 093 81 51',
        'tg': '@malkysha1',
        'hours': 'По договорённости',
        'services': 'Медицинская страховка для студентов',
        'price': '1200 рублей'
    },
    'medbook': {
        'name': 'Оформление медкнижки',
        'address': 'улица Куйбышева, 50А, 614016 • этаж 1',
        'phone': '+7 (342) 236-48-04',
        'hours': 'Пн-Пт 9:00-18:00',
        'services': 'Медицинская книжка для учёбы и работы',
        'price': '600 рублей'
    },
    'skala': {
        'name': 'Фитнес клуб "Скала" (для студентов ПНИПУ)',
        'address': 'улица Пушкина, 72 • этаж 2',
        'phone': '+7 (342) 203-34-90',
        'hours': 'Пн-Вс 7:00-23:00',
        'services': 'Тренажёрный зал, групповые занятия',
        'price': '4500 рублей за 10 месяцев (для студентов ПНИПУ)',
        'site': 'perm.skala-sportclub.ru'
    }
}

CATEGORIES = {
    'mfc': '🏛 МФЦ Перми',
    'insurance': '📄 Страхование',
    'medbook': '📋 Медкнижка',
    'fitness': '💪 Фитнес для студентов ПНИПУ'
}

@router.message(Command('орг'))
@router.message(F.text == "🏢 Организации")
async def show_org_menu(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=CATEGORIES['mfc'], callback_data="cat_mfc")],
        [InlineKeyboardButton(text=CATEGORIES['insurance'], callback_data="cat_insurance")],
        [InlineKeyboardButton(text=CATEGORIES['medbook'], callback_data="cat_medbook")],
        [InlineKeyboardButton(text=CATEGORIES['fitness'], callback_data="cat_fitness")],
        [InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")]
    ])
    
    await message.answer(
        "🏢 ОРГАНИЗАЦИИ ПЕРМИ\n\n"
        "Выбери категорию:",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "cat_mfc")
async def show_mfc(callback: CallbackQuery):
    if not callback.message:
        await callback.answer()
        return
    
    mfc_list = [
        ('mfc_1', '📍 Космонавтов, 65'),
        ('mfc_2', '📍 Попова, 23'),
        ('mfc_3', '📍 Куйбышева, 9'),
        ('mfc_4', '📍 Ленина, 92')
    ]
    
    text = "🏛 МФЦ ПЕРМИ\n\n"
    buttons = []
    
    for key, desc in mfc_list:
        org = ORGANIZATIONS[key]
        text += f"• {org['name']}\n"
        buttons.append([
            InlineKeyboardButton(text=org['name'][:30], callback_data=f"detail_{key}")
        ])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_org")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "cat_insurance")
async def show_insurance(callback: CallbackQuery):
    if not callback.message:
        await callback.answer()
        return
    
    org = ORGANIZATIONS['insurance_malkysha']
    
    text = f"📄 {org['name']}\n\n"
    text += f"📍 Адрес: {org['address']}\n"
    text += f"📞 Телефон: {org['phone']}\n"
    text += f"📱 Telegram: {org['tg']}\n"
    text += f"🕒 Часы: {org['hours']}\n"
    text += f"📋 Услуги: {org['services']}\n"
    text += f"💰 Цена: {org['price']}\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_org")]
    ])
    
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "cat_medbook")
async def show_medbook(callback: CallbackQuery):
    if not callback.message:
        await callback.answer()
        return
    
    org = ORGANIZATIONS['medbook']
    
    text = f"📋 {org['name']}\n\n"
    text += f"📍 Адрес: {org['address']}\n"
    text += f"📞 Телефон: {org['phone']}\n"
    text += f"🕒 Часы: {org['hours']}\n"
    text += f"📋 Услуги: {org['services']}\n"
    text += f"💰 Цена: {org['price']}\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_org")]
    ])
    
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "cat_fitness")
async def show_fitness(callback: CallbackQuery):
    if not callback.message:
        await callback.answer()
        return
    
    org = ORGANIZATIONS['skala']
    
    text = f"💪 {org['name']}\n\n"
    text += f"📍 Адрес: {org['address']}\n"
    text += f"📞 Телефон: {org['phone']}\n"
    text += f"🕒 Часы: {org['hours']}\n"
    text += f"📋 Услуги: {org['services']}\n"
    text += f"💰 Цена: {org['price']}\n"
    text += f"🌐 Сайт: {org['site']}\n\n"
    text += "🎓 Специально для студентов ПНИПУ!"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_org")]
    ])
    
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("detail_"))
async def show_org_detail(callback: CallbackQuery):
    if not callback.message or not callback.data:
        await callback.answer()
        return
    
    org_key = callback.data.replace("detail_", "")
    
    if org_key not in ORGANIZATIONS:
        await callback.answer("Организация не найдена")
        return
    
    org = ORGANIZATIONS[org_key]
    
    text = f"🏢 {org['name']}\n\n"
    text += f"📍 Адрес: {org['address']}\n"
    text += f"📞 Телефон: {org['phone']}\n"
    text += f"🕒 Часы: {org['hours']}\n"
    text += f"📋 Услуги: {org['services']}\n"
    
    if org.get('price'):
        text += f"💰 Цены: {org['price']}\n"
    if org.get('site'):
        text += f"🌐 Сайт: {org['site']}\n"
    if org.get('tg'):
        text += f"📱 Telegram: {org['tg']}\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="cat_mfc")]
    ])
    
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "back_to_org")
async def back_to_org(callback: CallbackQuery):
    if not callback.message:
        await callback.answer()
        return
    
    await show_org_menu(callback.message)

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    if not callback.message:
        await callback.answer()
        return
    
    from .start import cmd_start
    await callback.message.answer("👋 Главное меню")
    await cmd_start(callback.message)
    await callback.answer()