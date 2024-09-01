from django.contrib.auth.models import Permission
from django.contrib.admin import site as admin_site
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Initialize and Sync"

    def handle(self, *args, **options):
        self.add_action_button_permissions()

    def add_action_button_permissions(self):
        for model, admin_class in admin_site._registry.items():
            if not hasattr(admin_class, 'action_buttons'):
                continue

            for action_button in admin_class.action_buttons:
                content_type = ContentType.objects.get_for_model(
                    model=model,
                )

                permission, created = Permission.objects.get_or_create(
                    codename=action_button.permission_codename,
                    content_type=content_type,
                    defaults={
                        "name": action_button.permission_name,
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"permission: {permission.name} created"))
