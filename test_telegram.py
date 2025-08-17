"""
Тестовый файл для проверки работы модуля telegram.py
"""

import os
import django

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from core.telegram import send_telegram_message

if __name__ == "__main__":
    # Тестовое сообщение
    test_message = "Тестовое сообщение из Django приложения!"
    
    # Отправляем сообщение
    success = send_telegram_message(test_message)
    
    if success:
        print("Сообщение успешно отправлено!")
    else:
        print("Не удалось отправить сообщение. Проверьте настройки TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID.")
