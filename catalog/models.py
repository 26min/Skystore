from django.db import models

# Модель категории
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")  # type: ignore
    description = models.TextField(verbose_name="Описание", blank=True, null=True)  # type: ignore

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


# Модель продукта
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")  # type: ignore
    description = models.TextField(verbose_name="Описание")  # type: ignore
    image = models.ImageField(
        upload_to='products/',
        verbose_name="Изображение",
        blank=True,
        null=True
    )  # type: ignore
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name='products'
    )  # type: ignore
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за покупку"
    )  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # type: ignore
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")  # type: ignore

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-created_at']

    def __str__(self):
        return self.name