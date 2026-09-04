import os

from catalog.models import Category, Product
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Загружает тестовые данные из фикстур в базу данных"

    def handle(self, *args, **options):
        # Очищаем базу данных, удаляем старые данные
        self.stdout.write(self.style.WARNING("Удаление старых данных..."))
        Category.objects.all().delete()
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Старые данные удалены!"))

        # Загружаем данные из фикстур
        self.stdout.write(self.style.WARNING("Загрузка новых данных из фикстур..."))

        # Путь к папке с фикстурами
        fixtures_dir = os.path.join("catalog", "fixtures")

        # Проверяем, есть ли фикстуры
        categories_fixture = os.path.join(fixtures_dir, "categories.json")
        products_fixture = os.path.join(fixtures_dir, "products.json")

        if os.path.exists(categories_fixture):
            call_command("loaddata", "catalog/fixtures/categories.json", verbosity=0)
            self.stdout.write(self.style.SUCCESS("Категории загружены!"))

        if os.path.exists(products_fixture):
            call_command("loaddata", "catalog/fixtures/products.json", verbosity=0)
            self.stdout.write(self.style.SUCCESS("Продукты загружены!"))

        self.stdout.write(self.style.SUCCESS("✅ Все данные успешно загружены!"))
