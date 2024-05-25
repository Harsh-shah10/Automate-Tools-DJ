from django.core.management import BaseCommand
from dataentry.models import Student


class Command(BaseCommand):
    help = "This cmd helps to insert Student data into DB"

    def handle(self, *args, **kwargs): # Main logic
        users_data = [
            {'roll_no': 111, 'name': 'Harsh', 'age': 12},
            {'roll_no': 112, 'name': 'John', 'age': 15},
            {'roll_no': 113, 'name': 'Alice', 'age': 14},
            # Add more users as needed
        ]
        for i in users_data:
            Student.objects.create(roll_no=i['roll_no'], name=i['name'], age=i['age'])
        self.stdout.write(self.style.SUCCESS("Data inserted Successfully !!"))
