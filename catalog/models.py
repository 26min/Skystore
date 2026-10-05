from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="products/", verbose_name="Изображение", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за покупку")

    is_published = models.BooleanField(default=False, verbose_name="Опубликован")

    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Владелец", related_name="products"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-created_at"]
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]

    def __str__(self):
        return self.name
