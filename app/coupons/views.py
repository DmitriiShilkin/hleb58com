from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import ListView, UpdateView, CreateView

from .forms import CouponForm, CouponApplyForm
from .models import Coupon


# Представление для просмотра всех промокодов
class CouponListView(PermissionRequiredMixin, ListView):
    model = Coupon
    ordering = '-valid_to'
    template_name = 'coupon/coupon_list.html'
    context_object_name = 'coupons'
    paginate_by = 10
    # требование права на просмотр
    permission_required = ('coupons.view_coupon',)
    raise_exception = True


# Представление, создающее промокод
class CouponCreateView(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму,
    form_class = CouponForm
    # модель промокода,
    model = Coupon
    # шаблон, в котором используется форма,
    template_name = 'coupon/coupon_create.html'
    success_url = reverse_lazy('coupon_list')
    # требование права на добавление
    permission_required = ('coupons.add_coupon',)
    raise_exception = True


# Представление, изменяющее промокод
class CouponUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = CouponForm
    model = Coupon
    template_name = 'coupon/coupon_update.html'
    success_url = reverse_lazy('coupon_list')
    # требование права на изменение
    permission_required = ('coupons.change_coupon',)
    raise_exception = True


# Представление, активирующее промокод
@require_POST
@login_required
def coupon_apply_view(request):
    now = timezone.now().date()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        try:
            coupon = Coupon.objects.get(name__iexact=name,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        is_active=True)
            request.session['coupon_id'] = coupon.id
        except ObjectDoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart_detail')
