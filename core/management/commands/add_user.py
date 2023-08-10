from django.core.management.base import BaseCommand
from core.models import User

class Command(BaseCommand):
    help = 'Create seed data'

    def handle(self, *args, **kwargs):
        try:
            if User.objects.all():
                pass
            else:
                user = User.objects.create(first_name="admin",last_name="user"email="admin@domain.com",username ='admin@domain.com',is_staff=True,is_superuser=True)
                user.is_superuser=True
                user.set_password('superuser')
                user.save()
                self.stdout.write("Seed data created successfully")
        except Exception as e:
            self.stdout.write("Error in creating seed data %s" % str(e))
            
            
