from catalog.models import Product
from django.core.cache import cache


def get_products_by_category(category_id):
    """Возвращает список продуктов в категории (с кэшированием)"""
    cache_key = f"category_{category_id}"

    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    products = Product.objects.filter(category_id=category_id, is_published=True)
    data = list(products.values("id", "name", "price", "description"))

    cache.set(cache_key, data, timeout=600)
    return data


def get_all_products():
    """Возвращает список всех опубликованных продуктов (с кэшированием)"""
    cache_key = "all_products"

    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    products = Product.objects.filter(is_published=True)
    data = list(
        products.values(
            "id",
            "name",
            "price",
            "description",
            "image",
            "category_id",
            "owner_id",
        )
    )

    cache.set(cache_key, data, timeout=300)
    return data
