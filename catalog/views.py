from catalog.models import Product
from django.shortcuts import render


def home(request):
    """Главная страница — показывает все товары из базы"""
    products = Product.objects.all().order_by("-created_at")
    context = {"products": products}
    return render(request, "catalog/home.html", context)


def contacts(request):
    """Страница контактов — показывает контактную информацию"""
    return render(request, "catalog/contacts.html")
