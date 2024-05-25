from django.core.management import BaseCommand


# python manage.py hello 
class Command(BaseCommand):
    
    # python manage.py hello --help
    help = "This is my commands"

    def handle(self, *args, **kwargs): # Main logic
        self.stdout.write("Hello world !!")