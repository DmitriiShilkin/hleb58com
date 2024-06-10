import os
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


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


def send_mails(order_uid, customer_emails, template, subject, status, wish_date, created_at):
    # указываем какой шаблон брать за основу и преобразовываем его в строку для отправки клиенту
    html_context = render_to_string(
        template,
        {
            'order_uid': order_uid,
            'status': status,
            'wish_date': wish_date,
            'created_at': created_at
        }
    )

    msg = EmailMultiAlternatives(
        # тема письма
        subject=subject,
        # тело пустое, потому что мы используем шаблон
        body='',
        # адрес отправителя
        from_email=settings.DEFAULT_FROM_EMAIL,
        # список адресатов
        to=customer_emails,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send(fail_silently=False)
