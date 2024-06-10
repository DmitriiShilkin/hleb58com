from collections import defaultdict

from django.utils import timezone

from .models import Order


# поиск заказов и продуктов в них за указанное количество дней
def get_new_orders_products(days):
    # определяем текущий день
    today = timezone.now().today()
    # определяем интервал времени от прошедшего до текущего дня
    time_ago = today - timezone.timedelta(days=days)
    # ищем заказы за указанный временной интервал и считаем их количество
    orders = Order.objects.filter(created_at__gte=time_ago)
    products = defaultdict(int)
    for order in orders:
        for item in order.items.all():
            products[item.product.name] += item.amount

    return products, orders.count()


def get_correct_words_endings(days):
    if (days % 100) % 10 == 1 or days % 10 > 4 or days % 10 == 0:
        last_end = 'ие'
        day_end = 'ней'
    elif days % 10 in (2, 3, 4):
        last_end = 'ие'
        day_end = 'ня'
    elif days % 10 == 1:
        last_end = 'ий'
        day_end = 'ень'
    else:
        last_end = 'ие'
        day_end = 'ней'

    return last_end, day_end
