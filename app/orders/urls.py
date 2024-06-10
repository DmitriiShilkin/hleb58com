from django.urls import path

from .views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderUpdateByStaffView,
    order_cancel_view,
    order_cancel_confirmation_view,
    order_repeat_view,
    stats_view,
    ReportView,
)

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/staffupdate/', OrderUpdateByStaffView.as_view(), name='order_update_by_staff'),
    path('<int:pk>/cancel/', order_cancel_view, name='order_cancel'),
    path('<int:pk>/cancel_confirmation/', order_cancel_confirmation_view, name='order_cancel_confirmation'),
    path('<int:pk>/repeat/', order_repeat_view, name='order_repeat'),
    path('stats/<int:days>/', stats_view, name='stats'),
    path('report/', ReportView.as_view(), name='report'),
]
