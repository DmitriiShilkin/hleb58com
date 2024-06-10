from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import PostForm, CategoryForm
from .models import Post, Category
from .tasks import force_majeure_mail_notification


class PostListView(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


# Представление для просмотра отдельной публикации
class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'


# Представление, создающее новость
class PostCreateView(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму,
    form_class = PostForm
    # модель новостей,
    model = Post
    # шаблон, в котором используется форма,
    template_name = 'news/post_create.html'
    success_url = reverse_lazy('post_list')
    # и требование права на добавление новости.
    permission_required = ('news.add_post',)
    raise_exception = True

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        result = super().form_valid(form)
        categories = post.category.all().values_list('name', flat=True)
        if 'Форс-мажор' in categories:
            force_majeure_mail_notification.delay()
        return result


# Представление, изменяющее новость
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_update.html'
    success_url = reverse_lazy('post_list')
    # требование права на изменение новости
    permission_required = ('news.change_post',)
    raise_exception = True

    def form_valid(self, form):
        post = form.save(commit=False)
        post.modified_at = timezone.now()
        return super().form_valid(form)


# Представление для просмотра всех категорий
class CategoryListView(PermissionRequiredMixin, ListView):
    model = Category
    ordering = '-created_at'
    template_name = 'news/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10
    # требование права на просмотр категорий
    permission_required = ('news.view_category',)
    raise_exception = True


# Представление, создающее категорию
class CategoryCreateView(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму,
    form_class = CategoryForm
    # модель категории,
    model = Category
    # шаблон, в котором используется форма,
    template_name = 'news/category_create.html'
    success_url = reverse_lazy('post_category_list')
    # требование права на добавление категорий
    permission_required = ('news.add_category',)
    raise_exception = True


# Представление, изменяющее категорию
class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = CategoryForm
    model = Category
    template_name = 'news/category_update.html'
    success_url = reverse_lazy('post_category_list')
    # требование права на изменение категории
    permission_required = ('news.change_category',)
    raise_exception = True

    def form_valid(self, form):
        post = form.save(commit=False)
        post.modified_at = timezone.now()
        return super().form_valid(form)
