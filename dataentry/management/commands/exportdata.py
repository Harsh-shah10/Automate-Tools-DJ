from django.core.management.base import CommandParser, BaseCommand
from django.apps import apps
import datetime, csv
from dataentry.utils import generate_csv_file_path


class Command(BaseCommand):
    help = "This cms helps to export any model data"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('model_name', type=str, help='Pass valid model_name !!')

    def handle(self, *args, **kwargs): # Main logic
        model_name = kwargs['model_name'].capitalize()

        get_model = None
        for installed_app in apps.get_app_configs():
            try:
                get_model = apps.get_model(app_label=installed_app.label, model_name=model_name)
                break # Stop the execution once the model is found !!
            except LookupError:
                pass

        if not get_model:
            self.stderr.write(f"Model : {model_name} cound note be found !!")
            return

        # Fetching the data from the db
        all_records = get_model.objects.all()  
        if not all_records:
            self.stdout.write(self.style.WARNING("No data available !!"))
            return      

        file_path = generate_csv_file_path(model_name)

        # create a CSV file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # create csv header
            fields = [field.name for field in get_model._meta.fields]
            writer.writerow(fields)

            # write data to CSV
            for i in all_records:
                writer.writerow([getattr(i, field.name) for field in get_model._meta.fields])

        self.stdout.write(self.style.SUCCESS("Data Exported Successfully !!"))

     
        

        