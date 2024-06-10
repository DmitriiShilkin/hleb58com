from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    product_create_view,
    product_update_view,
    make_visible_view,
    make_invisible_view,
    InvisibleListView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
)

urlpatterns = [
    # связываем представления с URL-адресами страниц
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', product_create_view, name='product_create'),
    path('<int:pk>/update/', product_update_view, name='product_update'),
    path('<int:pk>/visible/', make_visible_view, name='product_visible'),
    path('<int:pk>/invisible/', make_invisible_view, name='product_invisible'),
    path('invisible/', InvisibleListView.as_view(), name='invisible_list'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
]
