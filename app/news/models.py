from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from sign.models import CustomUser


class Category(models.Model):
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False
    )
    modified_at = models.DateTimeField(
        editable=False,
        blank=True,
        null=True
    )
    name = models.CharField(
        verbose_name='Название',
        unique=True,
        max_length=20,
        validators=[
            MinLengthValidator(4),
        ]
    )
    description = models.CharField(
        verbose_name='Описание',
        blank=True,
        null=True,
        max_length=254
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Создан',
        default=timezone.now,
        editable=False
    )
    modified_at = models.DateTimeField(
        verbose_name='Изменен',
        editable=False,
        blank=True,
        null=True
    )
    headline = models.CharField(
        verbose_name='Заголовок',
        max_length=128,
        validators=[
            MinLengthValidator(20),
        ]
    )
    content = models.TextField(
        verbose_name='Содержание',
        validators=[
            MinLengthValidator(50),
        ]
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET(None),
        verbose_name='Автор'
    )
    category = models.ManyToManyField(
        Category,
        through='PostCategory',
        related_name='post',
        verbose_name='Категория'
    )

    def preview(self):
        return self.content[:124] + '...'

    def __str__(self):
        return f'{self.headline}: {self.content[:20]}'

    # функция reverse позволяет нам указывать не путь вида /news/…, а название пути, которое мы задали в файле urls.py
    # для аргумента name
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
