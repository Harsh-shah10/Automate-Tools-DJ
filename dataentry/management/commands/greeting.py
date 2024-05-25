from django.core.management import BaseCommand
from django.core.management.base import CommandParser


# python manage.py greeting harry
class Command(BaseCommand):
    
    # python manage.py greeting --help
    help = "This command greets the User"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('name', type=str, help='Pass name !!')

    def handle(self, *args, **kwargs): # Main logic
        name = kwargs['name']
        greeting_msg = f"My name is {name} !!"
        
        self.stdout.write(greeting_msg)
        self.stderr.write(greeting_msg)
        self.stdout.write(self.style.WARNING(greeting_msg))
        self.stdout.write(self.style.SUCCESS(greeting_msg))
