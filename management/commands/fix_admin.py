from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Fix superuser permissions'
    
    def handle(self, *args, **options):
        User = get_user_model()
        
        # Find existing superuser
        superuser = User.objects.filter(is_superuser=True).first()
        
        if superuser:
            superuser.is_staff = True
            superuser.is_superuser = True  
            superuser.is_active = True
            superuser.save()
            self.stdout.write(f'Fixed permissions for: {superuser.username}')
        else:
            # Create new superuser
            User.objects.create_superuser(
                username='admin',
                email='Shaswatsinha05@gmail.com',
                password='Shaswat4120@'
            )
            self.stdout.write('Created new superuser: admin/admin123')