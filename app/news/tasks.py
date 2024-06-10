from celery import shared_task

from company.services import send_mails
from orders.models import Order


# задача, которая уведомляет клиента о форс-мажорах
@shared_task
def force_majeure_mail_notification(order=None, status=None, wish_date=None, created_at=None):
    orders = Order.objects.filter(is_complete=False)
    emails = []
    for order in orders:
        emails.append(order.customer.email)

    customer_emails = list(set(emails))
    template = 'news/mail/force_majeure_email.html'
    subject = 'Форс-мажор'

    send_mails(order, customer_emails, template, subject, status, wish_date, created_at)
