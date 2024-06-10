from django.urls import path

from .views import (
    CouponListView,
    CouponCreateView,
    CouponUpdateView,
    # CouponApplyView,
    coupon_apply_view,
)

urlpatterns = [
    # связываем представления с URL-адресами страниц
    path('', CouponListView.as_view(), name='coupon_list'),
    path('create/', CouponCreateView.as_view(), name='coupon_create'),
    path('<int:pk>/', CouponUpdateView.as_view(), name='coupon_update'),
    path('apply/', coupon_apply_view, name='coupon_apply'),
]
