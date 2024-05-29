import os
from django.conf import settings
import aiohttp


# отправка сообщения в Telegram
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


# функция для сохранения добавляемых файлов
def handle_uploaded_file(name, file):
    # формируем путь до директории для загрузки файла
    dir_name = f'{settings.MEDIA_ROOT}/upload/{name}'
    # если указанная директория не существует
    if not os.path.isdir(dir_name):
        # создаем ее
        os.mkdir(dir_name)
    # формируем путь для загрузки файла
    upload_to = f'{dir_name}/{file}'
    # сохраняем файл
    with open(upload_to, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return upload_to
