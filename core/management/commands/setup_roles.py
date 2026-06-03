from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


MANAGED_APPS = ['core', 'products', 'pages', 'contacts']


class Command(BaseCommand):
    help = 'Create Admin and Manager groups with default permissions.'

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        manager_group, _ = Group.objects.get_or_create(name='Manager')

        admin_group.permissions.set(Permission.objects.all())
        manager_permissions = Permission.objects.filter(content_type__app_label__in=MANAGED_APPS)
        manager_group.permissions.set(manager_permissions)

        self.stdout.write(self.style.SUCCESS('Created/updated Admin and Manager groups.'))
        self.stdout.write('Manager permissions include product gallery image add/change/delete permissions.')
        self.stdout.write('To create a manager: create a staff user, then add the user to the Manager group.')
