from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from mailing.models import Mailing, Message


class Command(BaseCommand):
    help = 'Creates initial groups and permissions'

    def handle(self, *args, **options):
        # Создаем группу менеджеров
        managers_group, created = Group.objects.get_or_create(name='Менеджеры')

        # Добавляем права для менеджеров
        content_type = ContentType.objects.get_for_model(Mailing)
        permissions = Permission.objects.filter(content_type=content_type)
        for perm in permissions:
            if perm.codename in ['set_is_active', 'launching_mailing']:
                managers_group.permissions.add(perm)

        content_type = ContentType.objects.get_for_model(Message)
        permissions = Permission.objects.filter(content_type=content_type)
        for perm in permissions:
            if perm.codename == 'set_update':
                managers_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Successfully initialized groups and permissions'))
