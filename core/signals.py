"""
Модуль сигналов для приложения core.
Содержит обработчики для автоматических действий при изменении данных.
"""

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Order
from .telegram import send_telegram_message
import logging

logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=Order.services.through)
def order_services_changed(sender, instance, action, **kwargs):
    """
    Обработчик сигнала m2m_changed для поля services модели Order.
    
    Отправляет уведомление в Telegram при добавлении услуг к заказу.
    """
    # Проверяем, что действие - это добавление связей
    if action == 'post_add':
        try:
            # Формируем информативное сообщение
            services_list = "\n".join([f"• {service.name} - {service.price}₽" 
                                     for service in instance.services.all()])
            
            message = f"""
📋 **НОВЫЙ ЗАКАЗ**

👤 **Клиент:** {instance.name}
📞 **Телефон:** {instance.phone}
✂️ **Мастер:** {instance.master.name if instance.master else 'Не назначен'}
📅 **Дата записи:** {instance.appointment_date.strftime('%d.%m.%Y %H:%M')}
📋 **Услуги:**
{services_list}

💬 **Комментарий:** {instance.comment if instance.comment else 'Нет комментария'}
"""
            
            # Отправляем сообщение в Telegram
            success = send_telegram_message(message.strip())
            if success:
                logger.info(f"Уведомление о заказе #{instance.id} успешно отправлено в Telegram")
            else:
                logger.error(f"Не удалось отправить уведомление о заказе #{instance.id} в Telegram")
                
        except Exception as e:
            logger.error(f"Ошибка в обработчике сигнала order_services_changed: {e}")
