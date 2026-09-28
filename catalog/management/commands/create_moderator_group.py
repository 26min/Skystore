from catalog.models import Product
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" с нужными правами'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Модератор продуктов")

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана.'))
        else:
            self.stdout.write(self.style.WARNING("Группа уже существует, обновляем права."))

        content_type = ContentType.objects.get_for_model(Product)

        try:
            can_unpublish = Permission.objects.get(codename="can_unpublish_product", content_type=content_type)
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR("Право can_unpublish_product не найдено!"))
            return

        try:
            can_delete = Permission.objects.get(codename="delete_product", content_type=content_type)
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR("Право delete_product не найдено!"))
            return

        group.permissions.add(can_unpublish, can_delete)
        self.stdout.write(self.style.SUCCESS("Права назначены группе."))

        self.stdout.write(self.style.SUCCESS("✅ Готово!"))
