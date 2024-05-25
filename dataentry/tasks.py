from celery import shared_task
import time
from django.core.management import call_command
from django.conf import settings
from django.core.mail import EmailMessage
from .utils import generate_csv_file_path

@shared_task
def test_celery():
    time.sleep(10)
    return 'Task executed !!'


@shared_task
def send_email(mail_subject, message, to_email, attachments=None):
    mail = EmailMessage(mail_subject, message, settings.DEFAULT_FROM_EMAIL, to=[to_email])
    
    # Send email as attachment
    if attachments:
        mail.attach_file(attachments)
    
    mail.send()
    return 'Email Send successfully !!'


@shared_task
def import_data_task(file_path, table_name):
    try:
        call_command('importdata', file_path, table_name)

        # Send Email to user once the Import us successfull
        send_email('CSV File Imported Successfull', 'Your excel sheet has been imported successfully !!', settings.DEFAULT_TO_EMAIL)
    except Exception as e:
        raise e
    return 'Import Data from CSV task executed !!'


@shared_task
def export_data_task(table_name):
    try:
        call_command('exportdata', table_name)

        # Seding file as attachment
        file_path = generate_csv_file_path(table_name)

        # Send Email to user once the Import us successfull
        send_email('Table exported Successfull', f'Your excel sheet for {table_name} table has been exported successfully !!. Please find the attachment below', settings.DEFAULT_TO_EMAIL, file_path)
    except Exception as e:
        raise e
    return 'Exporting Data from Table task executed !!'
