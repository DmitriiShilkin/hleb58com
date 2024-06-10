from django.urls import path

from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/category/', CategoryListView.as_view(), name='post_category_list'),
    path('post/category/create/', CategoryCreateView.as_view(), name='post_category_create'),
    path('post/category/<int:pk>', CategoryUpdateView.as_view(), name='post_category_update'),
]
