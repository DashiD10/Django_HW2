"""
Модуль для отправки сообщений в Telegram.
"""

import asyncio
from django.conf import settings
from telegram import Bot
from telegram.error import TelegramError
import logging

logger = logging.getLogger(__name__)


async def send_telegram_message_async(message: str) -> bool:
    """Асинхронно отправляет сообщение в Telegram чат через бота."""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    if not bot_token or not chat_id:
        logger.error("TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не заданы в настройках")
        return False
    
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Сообщение успешно отправлено в Telegram: {message[:50]}...")
        return True
        
    except TelegramError as e:
        logger.error(f"Ошибка при отправке сообщения в Telegram: {e}")
        return False
    except Exception as e:
        logger.error(f"Неожиданная ошибка при отправке сообщения в Telegram: {e}")
        return False


def send_telegram_message(message: str) -> bool:
    """Отправляет сообщение в Telegram чат через бота."""
    try:
        return asyncio.run(send_telegram_message_async(message))
    except Exception as e:
        logger.error(f"Ошибка при запуске асинхронной функции отправки сообщения: {e}")
        return False
