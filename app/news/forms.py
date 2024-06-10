from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'headline',
            'content',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        headline = cleaned_data.get("headline")
        content = cleaned_data.get("content")

        if headline == content:
            raise ValidationError(
                "Заголовок не должен быть идентичен содержанию!"
            )
        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
            'description',
        ]
