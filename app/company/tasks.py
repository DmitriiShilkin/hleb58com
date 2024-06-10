import os
from celery import shared_task
from django.conf import settings
import aiohttp


# отправка сообщения в Telegram
@shared_task
async def send_message(title, name, phone_number, email_link, text):
    async with aiohttp.ClientSession() as session:
        # команда для отправки сообщения в телеграм
        url = f'https://api.telegram.org/bot{settings.TOKEN}/sendMessage'

        # если переход выполнен по ссылке "Написать нам"
        if title == 'Написать нам':
            # формируем сообщение
            message = f'Заголовок: {title},\n\
Фамилия Имя Отчество: {name},\n\
Номер телефона: +7{phone_number},\n\
Email: {email_link},\n\
Текст сообщения: {text}'
            # задаем параметры передачи сообщения
            params = {'chat_id': settings.CHAT_ID, 'text': message}
        # если переход выполнен по ссылке "Стать поставщиком"
        else:
            # получаем имя прикрепленного файла с коммерческим предложением из полного пути
            file_name = os.path.basename(email_link)
            # формируем сообщение
            message = f'Заголовок: {title},\n\
Наименование организации: {name},\n\
Номер телефона: +7{phone_number},\n\
Коммерческое предложение: <a href="{email_link}">{file_name}</a>,\n\
Текст сообщения: {text}'
            # задаем параметры передачи сообщения
            params = {'chat_id': settings.CHAT_ID, 'text': message, 'parse_mode': 'html'}

        async with session.post(url, data=params) as response:
            await response.json()   # Эта строка отсылает сообщение
