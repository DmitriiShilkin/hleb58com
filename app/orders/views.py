import datetime
# импорт библиотеки для работы с файлами формата MS-Excel
import xlwt

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView

from .forms import (
    OrderCreateForm,
    OrderUpdateForm,
    OrderUpdateByStaffForm,
    OrderRepeatForm
)
from .models import Order, OrderItem
from .services import get_new_orders_products, get_correct_words_endings
from .tasks import (
    order_telegram_notification,
    order_mail_notification,
)

from cart.cart import Cart


# Представление для просмотра заказов
class OrderListView(PermissionRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    ordering = '-created_at'
    template_name = 'order/order_list.html'
    # требование права на просмотр заказа.
    permission_required = ('orders.view_order',)
    raise_exception = True
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().order_by(self.ordering)

        return Order.objects.filter(customer=self.request.user).order_by(self.ordering)


# Представление для просмотра заказа
class OrderDetailView(PermissionRequiredMixin, DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'
    # требование права на просмотр заказа.
    permission_required = ('orders.view_order',)
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_repeat_form = OrderRepeatForm()
        context['order_repeat_form'] = order_repeat_form
        return context

    def get_permission_required(self):
        self.object = self.get_object()
        if not (
                self.request.user == self.object.customer or
                self.request.user.is_staff or
                self.request.user.is_superuser
        ):
            content = f'''
                <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
            '''
            return HttpResponse(content=content)
        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms


# Представление, создающее заказ
class OrderCreateView(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму,
    form_class = OrderCreateForm
    model = Order
    # шаблон, в котором используется форма,
    template_name = 'order/order_create.html'
    success_url = reverse_lazy('order_list')
    # требование права на добавление заказа.
    permission_required = ('orders.add_order',)
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        return context

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save(commit=False)
        order.customer = self.request.user
        if cart.coupon:
            order.coupon = cart.coupon
            order.discount = cart.coupon.discount
        result = super().form_valid(form)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                price=item["price"],
                amount=item["quantity"]
            )
        cart.clear()
        # отправить сообщение менеджерам в телеграм о новом заказе
        order_telegram_notification.delay(order.uid, 'new_order')
        # отправить сообщение клиенту на почту о новом заказе
        order_mail_notification.delay(
            order.uid, order.get_status_display(), order.wish_date_at, 'new_order'
        )
        return result


# Представление, изменяющее заказ для покупателя
class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = OrderUpdateForm
    model = Order
    template_name = 'order/order_update.html'
    success_url = reverse_lazy('order_list')
    # требование права на изменение заказа
    permission_required = ('orders.change_order',)
    raise_exception = True

    def get_permission_required(self):
        self.object = self.get_object()
        if not (
                self.request.user == self.object.customer or
                self.request.user.is_staff or
                self.request.user.is_superuser
        ):
            content = f'''
                <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
            '''
            return HttpResponse(content=content)
        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def form_valid(self, form):
        order_db = self.get_object()
        order = form.save(commit=False)
        if order.wish_date_at != order_db.wish_date_at:
            order.modified_at = timezone.now()
            # отправить сообщение менеджерам в телеграм, что желаемая дата изменена
            order_telegram_notification.delay(order.uid, 'wish_date_changed')
            # отправить сообщение клиенту на почту, что желаемая дата изменена
            order_mail_notification.delay(
                order_db.uid, order_db.get_status_display(), order.wish_date_at, 'wish_date_changed'
            )
        return super().form_valid(form)


# Представление, изменяющее заказ для сотрудников
class OrderUpdateByStaffView(PermissionRequiredMixin, UpdateView):
    form_class = OrderUpdateByStaffForm
    model = Order
    template_name = 'order/order_update.html'
    success_url = reverse_lazy('order_list')
    # требование права на изменение заказа
    permission_required = ('orders.change_order',)
    raise_exception = True

    def get_permission_required(self):
        self.object = self.get_object()
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            content = f'''
                <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
            '''
            return HttpResponse(content=content)
        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def form_valid(self, form):
        order_db = self.get_object()
        order = form.save(commit=False)
        if order.status != order_db.status:
            order.modified_at = timezone.now()
            match order.status:
                case 'DLV':
                    # отправить сообщение клиенту на почту, что заказ передан в доставку
                    order_mail_notification.delay(
                        order_db.uid, order.get_status_display(), order_db.wish_date_at, 'status_changed'
                    )
                case 'CAN':
                    # отправить сообщение клиенту на почту, что заказ отменен
                    order_mail_notification.delay(
                        order_db.uid, order.get_status_display(), order_db.wish_date_at, 'status_changed'
                    )
                case 'FIN':
                    order.finish_order()
                    # отправить сообщение клиенту на почту, что заказ завершен
                    order_mail_notification.delay(
                        order_db.uid, order.get_status_display(), order_db.wish_date_at, 'status_changed'
                    )
        return super().form_valid(form)


# Представление, отменяющее заказ
@permission_required('orders.change_order', raise_exception=True)
def order_cancel_view(request, pk):
    # получаем активный заказ
    order = Order.objects.get(id=pk)
    if not (
            request.user == order.customer or
            request.user.is_staff or
            request.user.is_superuser
    ):
        content = f'''
            <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
        '''
        return HttpResponse(content=content)

    # отменяем
    try:
        order.set_canceled()
    except ValueError as e:
        content = f'''
            <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">Ошибка: {e}</p>
        '''
        return HttpResponse(content=content)
    # отправить сообщение менеджерам в телеграм, что заказ отменен клиентом
    order_telegram_notification.delay(order.uid, 'status_changed')
    # отправить сообщение клиенту на почту, что заказ отменен
    order_mail_notification.delay(
        order.uid, order.get_status_display(), order.wish_date_at, 'status_changed'
    )
    return redirect('order_list')


# Представление, для подтверждения отмены заказа
@permission_required('orders.change_order', raise_exception=True)
def order_cancel_confirmation_view(request, pk):
    # получаем активный заказ
    order = Order.objects.get(id=pk)
    if not (
            request.user == order.customer or
            request.user.is_staff or
            request.user.is_superuser
    ):
        content = f'''
            <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
        '''
        return HttpResponse(content=content)

    return render(
        request,
        context={"order": order},
        template_name='order/order_cancel_confirmation.html'
    )


# Представление, копирующее заказ
@permission_required('orders.add_order', raise_exception=True)
def order_repeat_view(request, pk):
    # получаем активный заказ
    order = Order.objects.get(id=pk)
    if not (
            request.user == order.customer or
            request.user.is_staff or
            request.user.is_superuser
    ):
        content = f'''
            <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
        '''
        return HttpResponse(content=content)

    form = OrderRepeatForm()
    if request.method == 'POST':
        form = OrderRepeatForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = order.customer
            if order.coupon:
                new_order.coupon = order.coupon
                new_order.discount = order.coupon.discount
            new_order.save()
            for item in order.items.all():
                OrderItem.objects.create(
                    order=new_order,
                    product=item.product,
                    price=item.price,
                    amount=item.amount
                )
            # отправить сообщение менеджерам в телеграм о новом заказе
            order_telegram_notification.delay(order.uid, 'new_order')
            # отправить сообщение клиенту на почту о новом заказе
            order_mail_notification.delay(
                new_order.uid, new_order.get_status_display(), new_order.wish_date_at, 'new_order'
            )
            return redirect('order_list')

    return render(request, 'order/order_detail.html', {'form': form, 'order': order})


# представление для сохранения данных по заказам в файл xls
@permission_required('orders.view_order', raise_exception=True)
def stats_view(request, days):
    # получаем сотрудника
    if not (
            'management' in request.user.groups.all().values_list('name', flat=True) or
            request.user.is_superuser
    ):
        content = f'''
            <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
        '''
        return HttpResponse(content=content)
    # формат данных
    response = HttpResponse(content_type='application/ms-excel')
    # формируем текущую дату для добавления к имени файла
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    # задаем имя файла
    response['Content-Disposition'] = 'attachment; filename="product_stats_{}.xls"'.format(date)
    # кодировка в книге эксель
    wb = xlwt.Workbook(encoding='utf-8')
    # список ячеек шапки таблицы
    columns = ['Наименование', 'Количество за выбранный период', ]

    # добавляем лист в книгу
    # название листа книги
    last_end, day_end = get_correct_words_endings(days)
    sheet = f"Статистика за последн{last_end} {days} д{day_end}"
    ws = wb.add_sheet(sheet)
    # ширина колонок
    ws.col(0).width = 35 * 256
    ws.col(1).width = 35 * 256
    # обводка ячеек
    borders = xlwt.Borders()
    borders.left = xlwt.Borders().THIN
    borders.right = xlwt.Borders().THIN
    borders.top = xlwt.Borders().THIN
    borders.bottom = xlwt.Borders().THIN
    # выравнивание
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    # заливка ячеек
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 22

    # добавляем таблицу
    # шапка таблицы
    row_num = 0
    # параметры стиля оформления
    style1 = xlwt.XFStyle()
    style1.font.bold = True
    style1.borders = borders
    style1.pattern = pattern
    style1.alignment = alignment

    style2 = xlwt.XFStyle()
    style2.borders = borders

    style3 = xlwt.XFStyle()
    style3.font.bold = True
    style3.borders = borders
    style3.pattern = pattern

    # записываем шапку таблицы
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)

    # получаем данные о продуктах и заказах за указанное количество дней
    rows, last_row = get_new_orders_products(days)

    # записываем остальные строки таблицы
    for key, value in rows.items():
        row_num += 1
        # записываем столбцы текущей строки
        ws.write(row_num, 0, key, style2)
        ws.write(row_num, 1, value, style2)

    row_num += 2
    ws.write(row_num, 0, 'Суммарное количество заказов', style3)
    ws.write(row_num, 1, last_row, style3)

    # сохраняем книгу
    wb.save(response)
    return response


class ReportView(PermissionRequiredMixin, TemplateView):
    template_name = 'order/report.html'
    permission_required = ('orders.view_order',)
    raise_exception = True

    def get_permission_required(self):
        if not (
                'management' in self.request.user.groups.all().values_list('name', flat=True) or
                self.request.user.is_superuser
        ):
            content = f'''
                <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
            '''
            return HttpResponse(content=content)
        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms
