from catalog.models import Product
from django.shortcuts import get_object_or_404, render


def home(request):
    """Главная страница — список всех товаров"""
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/home.html', context)


def contacts(request):
    """Страница контактов"""
    return render(request, 'catalog/contacts.html')


# НОВЫЙ КОНТРОЛЛЕР ДЛЯ СТРАНИЦЫ ТОВАРА
def product_detail(request, pk):
    """
    Страница с подробной информацией о товаре.
    Получает pk (первичный ключ) из URL, находит товар в БД,
    если не найден — возвращает 404.
    """
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)
