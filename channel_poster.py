import sqlite3
import datetime
import asyncio
from aiogram import Bot

class ChannelPoster:
    def __init__(self, bot: Bot, channel_id: int):
        self.bot = bot
        self.channel_id = channel_id
    
    async def post_news(self, title: str, content: str, category: str = "новости"):
        """Публикует новость в канал"""
        text = f"📢 **{title}**\n\n{content}\n\n#{category}"
        
        message = await self.bot.send_message(self.channel_id, text)
        
        # Сохраняем в базу
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()
        cur.execute('''
        INSERT INTO channel_posts (post_id, title, content, category, date)
        VALUES (?, ?, ?, ?, ?)
        ''', (message.message_id, title, content, category, datetime.datetime.now().strftime("%d.%m.%Y")))
        conn.commit()
        conn.close()
        
        return message
    
    async def post_regular(self):
        """Публикует регулярные посты (можно запустить по расписанию)"""
        # Пример: пост о МФЦ
        await self.post_news(
            "🏛 МФЦ Перми",
            "ул. Куйбышева, 9\nтел: 8 (800) 234-32-75\nЧасы: Пн-Пт 9:00-20:00",
            "контакты"
        )
        
        # Пример: пост о страховке
        await self.post_news(
            "📄 Страховка для студентов",
            "Комсомольский пр., 84\n@malkysha1\n1200 рублей",
            "услуги"
        )
        
        # Пример: пост о фитнесе
        await self.post_news(
            "💪 Фитнес клуб Скала (для студентов ПНИПУ)",
            "ул. Пушкина, 72\n4500 руб за 10 месяцев\nperm.skala-sportclub.ru",
            "скидки"
        )