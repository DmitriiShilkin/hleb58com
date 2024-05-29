from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Product, Category, ProductImage
from .forms import ProductForm, CategoryForm


# Представление для просмотра всех продуктов
class ProductListView(ListView):
    model = Product
    context_object_name = 'visibles'
    ordering = '-created_at'
    template_name = 'products/product_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.filter(is_visible=True).order_by(self.ordering)


# Представление для просмотра скрытых продуктов
class InvisibleListView(PermissionRequiredMixin, ListView):
    model = Product
    context_object_name = 'invisibles'
    ordering = '-created_at'
    template_name = 'products/invisible_list.html'
    paginate_by = 10
    permission_required = ('products.view_product',)
    raise_exception = True

    def get_queryset(self):
        return Product.objects.filter(is_visible=False).order_by(self.ordering)


# Представление для просмотра конкретного продукта
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


# Представление, создающее продукт
@permission_required('products.add_product', raise_exception=True)
def product_create_view(request):
    ImageFormset = modelformset_factory(ProductImage, fields=('image',), extra=4, max_num=4)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)

        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.save()
            categories = form.cleaned_data['category']

            # добавляем категории в продукту
            if categories:
                product.category.set(categories)

            # проходим по добавленным в форму изображениям
            for f in formset:
                try:
                    # если есть изображение, забираем ссылку на него
                    new_image = f.cleaned_data['image']
                except Exception as e:
                    # иначе переходим на следующую форму с изображением
                    continue
                else:
                    # сохраняем добавленное изображение
                    image = ProductImage(product=product, image=new_image)
                    image.save()

            return redirect('product_list')
    else:
        form = ProductForm()
        formset = ImageFormset(queryset=ProductImage.objects.none())

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'products/product_create.html', context)


# Представление, изменяющее продукт
@permission_required('products.change_product', raise_exception=True)
def product_update_view(request, pk):
    ImageFormset = modelformset_factory(ProductImage, fields=('image',), extra=4, max_num=4)
    product = get_object_or_404(Product, id=pk)
    form = ProductForm(request.POST or None, instance=product)

    if request.method == 'POST':

        formset = ImageFormset(request.POST or None, request.FILES or None)

        if form.is_valid() and formset.is_valid():
            # form.save()
            product = form.save(commit=False)
            product.modified_at = timezone.now()
            product.save()

            # проходим по добавленным в форму изображениям
            for f in formset:
                try:
                    # если есть изображение, забираем ссылку на него
                    new_image = f.cleaned_data['image']
                except Exception as e:
                    # иначе переходим на следующую форму с изображением
                    continue
                else:
                    # если форма с изображением была не пустая
                    data = f.save(commit=False)
                    # получаем айди старого изображения
                    old_pk = data.pk
                    # проверяем есть ли загруженное изображение в БД
                    same_image = ProductImage.objects.filter(image=new_image).first()

                    # если загруженное изображение новое и форма пуста
                    if same_image is None and old_pk is None:
                        # сохраняем изображение
                        image_create = ProductImage(product=product, image=new_image)
                        image_create.save()

                    # если загруженное изображение новое и форма не пуста
                    if same_image is None and old_pk:
                        # заменяем старое изображение на новое
                        image_update = ProductImage.objects.filter(pk=old_pk).first()
                        # старый файл удаляем из хранилища
                        image_update.image.delete(save=False)
                        image_update.image = new_image
                        # сохраняем новое изображение
                        image_update.save()

                    # если выбран пункт "очисть" в форме с изображением
                    if not new_image:
                        # удаляем изображение
                        data.image.delete(save=False)
                        data.delete()

            return redirect('product_list')
    else:
        formset = ImageFormset(queryset=product.images.all())

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'products/product_update.html', context)


# Представление для просмотра всех категорий
class CategoryListView(PermissionRequiredMixin, ListView):
    model = Category
    ordering = '-created_at'
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10
    # требование права на просмотр категорий
    permission_required = ('products.view_category',)
    raise_exception = True


# Представление, создающее категорию
class CategoryCreateView(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму,
    form_class = CategoryForm
    # модель категории,
    model = Category
    # шаблон, в котором используется форма,
    template_name = 'products/category_create.html'
    success_url = reverse_lazy('category_list')
    # требование права на добавление категорий
    permission_required = ('products.add_category',)
    raise_exception = True


# Представление, изменяющее категорию
class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = CategoryForm
    model = Category
    template_name = 'products/category_update.html'
    success_url = reverse_lazy('category_list')
    # требование права на изменение категории
    permission_required = ('products.change_category',)
    raise_exception = True

    def post(self, request, *args, **kwargs):
        category = self.get_object()
        category.modified_at = timezone.now()
        # category.save(update_fields=['modified_at'])
        return super().post(request, *args, **kwargs)


# Представление, делающее продукт видимым
@permission_required('products.change_product', raise_exception=True)
def make_visible_view(request, pk):
    # получаем активный продукт
    product = Product.objects.get(id=pk)
    # меняем видимость
    product.make_visible()

    return redirect('invisible_list')


# Представление, делающее продукт не видимым
@permission_required('products.change_product', raise_exception=True)
def make_invisible_view(request, pk):
    # получаем активный продукт
    product = Product.objects.get(id=pk)
    # меняем видимость
    product.make_invisible()

    return redirect('product_list')
