from django.apps import apps
from django.db.utils import DataError 
from django.core.management.base import CommandError
import datetime, csv, os
from django.conf import settings



def get_all_custom_models():
    default_models = [
    'Group',
    'Permission',
    'ContentType',
    'Session',
    'Site',
    'Redirect',
    'LogEntry',
    ]

    all_tables = []
    for i in apps.get_models():
        if i.__name__ not in default_models:
            all_tables.append(i.__name__)
    # print(all_tables)
    return all_tables


def check_table_exists(table_name, export_data=False):
    get_model = None
    for installed_app in apps.get_app_configs():
        try:
            get_model = apps.get_model(app_label=installed_app.label, model_name=table_name)
            break # Stop the execution once the model is found !!
        except LookupError:
            pass
    
    if get_model is None:
        raise Exception("Table does not exist")

    get_model_queryset = get_model.objects.all()

    if not get_model_queryset.exists() and export_data:
        raise Exception("Table is empty")
        
    return get_model

    
def generate_csv_file_path(model_name):
    # set the file export folder path
    export_dir = 'exported_data'
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = f"export_{model_name}_data_{time_stamp}.csv"

    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path


def check_csv_errors(table_name, file_path):
    try:
        get_model = check_table_exists(table_name)
    except Exception as e:
        raise e 
    
    # Get all the columns/fields name of the model instance found !!
    model_fields = [field.name for field in get_model._meta.fields]

    # Open the CSV file and insert data into the specified table
    try:
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            
            # Fetch the CSV header/columns of CSV file
            csv_header = csv_reader.fieldnames
            if csv_header!= model_fields:
                raise DataError(f"CSV file fields does not match with {table_name} table fields !!")
    except Exception as e:
        raise e
    
    return get_model