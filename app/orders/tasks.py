import aiohttp
from celery import shared_task

from django.conf import settings

from company.services import send_mails

from .models import Order


# задача, которая уведомляет менеджеров в telegram
@shared_task
async def order_telegram_notification(order_uid, message_type):
    async with aiohttp.ClientSession() as session:
        order = Order.objects.get(uid=order_uid)
        # команда для отправки сообщения в телеграм
        url = f'https://api.telegram.org/bot{settings.TOKEN}/sendMessage'
        # формируем сообщение
        match message_type:
            case 'new_order':
                message = f'''Получен новый заказ:\n\
Номер заказа: {order_uid},\n\
На дату: {order.wish_date}.
'''
            case 'status_changed':
                message = f'''Статус заказа изменен:\n\
Номер заказа: {order_uid},\n\
Создан: {order.created_at},\n\
Статус: {order.get_status_display()}.
'''
            case 'wish_date_changed':
                message = f'''Дата заказа изменена:\n\
Номер заказа: {order_uid},\n\
Создан: {order.created_at},\n\
Новая дата: {order.wish_date}.
            '''
        # задаем параметры передачи сообщения
        params = {'chat_id': settings.CHAT_ID, 'text': message}

    async with session.post(url, data=params) as response:
        await response.json()  # Эта строка отсылает сообщение


# задача, которая уведомляет клиента по email
@shared_task
def order_mail_notification(order_uid, status, wish_date, message_type):
    order = Order.objects.get(uid=order_uid)
    customer_emails = [order.customer.email]
    match message_type:
        case 'new_order':
            template = 'order/mail/new_order_email.html'
            subject = 'Заказ оформлен'
        case 'status_changed':
            template = 'order/mail/order_change_status_email.html'
            subject = 'Статус заказа изменен'
        case 'wish_date_changed':
            template = 'order/mail/order_change_wish_date_email.html'
            subject = 'Дата заказа изменена'

    send_mails(order_uid, customer_emails, template, subject, status, wish_date, order.created_at)
