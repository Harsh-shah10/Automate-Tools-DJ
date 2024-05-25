from django.core.management.base import CommandParser, BaseCommand
from dataentry.models import Student
import datetime, csv
from django.apps import apps

from dataentry.utils import check_csv_errors

class Command(BaseCommand):
    help = "This cmd helps to import data from CSV into DB Table"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('table_name', type=str, help='Name of the table to insert data into')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        table_name = kwargs['table_name']
        get_model = check_csv_errors(table_name, file_path)

        # Open the CSV file and insert data into the specified table
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                # Create an instance of the model with the row data
                instance = get_model(**row)
                instance.save()

        self.stdout.write(self.style.SUCCESS("Data inserted Successfully !!"))
        return
