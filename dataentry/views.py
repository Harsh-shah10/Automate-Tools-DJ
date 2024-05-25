from django.shortcuts import render, redirect, HttpResponse
from .utils import get_all_custom_models, check_csv_errors, check_table_exists
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages

# Import cekrey tasks 
from .tasks import import_data_task, send_email, export_data_task

# Create your views here.
def import_data(request):
    if request.method == 'POST':
        csv_file_path = request.FILES.get('csv_file')
        table_name = request.POST.get('table')
        # print(file_path, table_name)

        # Store the file inside the upload model
        file_upload = Upload.objects.create(file=csv_file_path, model_name=table_name)

        # constructing the full path
        relative_path = str(file_upload.file.url)
        base_url = str(settings.BASE_DIR)
        file_path = base_url + relative_path

        try:
            check_csv_errors(table_name, file_path)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')

        # Using celery for tasks to run task in background
        import_data_task.delay(file_path, table_name) 
        messages.success(request, 'Your data is being imported. You will be notified once its completed !')
        return redirect('import_data')
    else:
        all_models =  get_all_custom_models()
        context = {"all_models":all_models}
    
    return render(request, 'dataentry/import_data.html',context)


def export_data(request):
    if request.method == 'POST':
        table_name = request.POST.get('table')

        try:
            check_table_exists(table_name, export_data=True)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('export_data')

        export_data_task.delay(table_name)
        messages.success(request, 'Data Exported Successfully !')
        return redirect('export_data')
    else:
        all_models =  get_all_custom_models()
        context = {"all_models":all_models}
    
    return render(request, 'dataentry/export_data.html',context)


def homepage(request):
    return render(request, 'index.html')


def celery_test(request):
    # test_celery.delay()
    send_email.delay('Test Subject', 'Jay shree ram !!', settings.DEFAULT_TO_EMAIL) # Send Test mail
    return HttpResponse("Execution success !!")