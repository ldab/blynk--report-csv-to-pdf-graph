import requests
from django import forms
from django.shortcuts import render
from django.http import HttpResponse

#django form upload stuff
from django.conf import settings
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from .graph import open_zip, read_csv, compress_it

#from graph import open_zip

from .models import Greeting

# Create your views here.
def index(request):
    #return HttpResponse('Hello from Python!')
    #UploadFileform()
    return render(request, 'index.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(path):
    open_zip(path)
    read_csv()
    compress_it()

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "Invoice_%s.pdf" %("12341231")
    content = "inline; filename='%s'" %(filename)
    download = request.GET.get("download")
    if download:
        content = "attachment; filename='%s'" %(filename)
    response['Content-Disposition'] = content
    return response
    #else: return HttpResponse("Not found")

    shutil.rmtree(tempFolder)

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
