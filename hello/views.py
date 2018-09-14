import requests
from django import forms
from django.shortcuts import render
from django.http import HttpResponse

#django form upload stuff
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import Greeting

# Create your views here.
def index(request):
    #return HttpResponse('Hello from Python!')
    #UploadFileform()
    return render(request, 'index.html')

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

