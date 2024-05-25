from django.core.management import BaseCommand
from dataentry.models import Student
import datetime, csv

class Command(BaseCommand):
    help = "This cmd helps to export Student data to CSV File"

    def handle(self, *args, **kwargs): # Main logic
        # fetch data from student table
        all_records = Student.objects.all()

        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
     
        file_path = f"export_student_data_{time_stamp}.csv"

        if not all_records:
            self.stdout.write(self.style.WARNING("No data available !!"))
            return

        # create a CSV file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # create csv header
            writer.writerow(['Roll no', 'Name', 'Age'])

            # write data to CSV
            for i in all_records:
                writer.writerow([i.roll_no, i.name, i.age])

        self.stdout.write(self.style.SUCCESS("Data Exported Successfully !!"))
