from django.contrib import admin

from .models import Product, ProductImage, Category


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    extra = 4
    max_num = 4


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model = Product


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category)
