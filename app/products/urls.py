from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    product_create_view,
    product_update_view,
    make_visible_view,
    make_invisible_view,
    InvisibleListView,
)

urlpatterns = [
    # связываем представления с URL-адресами страниц
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', product_create_view, name='product_create'),
    path('product/<int:pk>/update/', product_update_view, name='product_update'),
    path('product/<int:pk>/visible/', make_visible_view, name='product_visible'),
    path('product/<int:pk>/invisible/', make_invisible_view, name='product_invisible'),
    path('invisible/', InvisibleListView.as_view(), name='invisible_list'),
]
