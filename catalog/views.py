# from catalog.models import Product
# from django.shortcuts import get_object_or_404, render
#
#
# def home(request):
#     """Главная страница — список всех товаров"""
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'catalog/home.html', context)
#
#
# def contacts(request):
#     """Страница контактов"""
#     return render(request, 'catalog/contacts.html')
#
#
# # НОВЫЙ КОНТРОЛЛЕР ДЛЯ СТРАНИЦЫ ТОВАРА
# def product_detail(request, pk):
#     """
#     Страница с подробной информацией о товаре.
#     Получает pk (первичный ключ) из URL, находит товар в БД,
#     если не найден — возвращает 404.
#     """
#     product = get_object_or_404(Product, pk=pk)
#     context = {'product': product}
#     return render(request, 'catalog/product_detail.html', context)

from django.views.generic import ListView, TemplateView, DetailView
from catalog.models import Product

class ProductListView(ListView):
    """Главная страница — список всех товаров."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    """Страница с подробной информацией о товаре."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ContactsView(TemplateView):
    """Страница контактов."""
    template_name = 'catalog/contacts.html'