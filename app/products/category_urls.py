from django.urls import path

from .views import (
    CategoryListView,
    CategoryUpdateView,
    CategoryCreateView,
)

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('create/', CategoryCreateView.as_view(), name='category_create'),
    path('<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
]
