# функция получения пути для сохранения фотографий, чтобы было понятно, к какому продукту они относятся
def get_image_path(instance, file):
    return f'images/{instance.product}/{file}'
