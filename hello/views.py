import requests
from django import forms
from django.shortcuts import render
from django.http import HttpResponse

#django form upload stuff
from django.conf import settings
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage

#from graph import open_zip

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
        filename = fs.save(myfile.name, myfile) # saves the file to `media` folder
        uploaded_file_url = fs.url(filename)    # gets the url
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #DO_THE_MAGIC(request.FILES['file'])     #python function goes here!!!!!!!!
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def upload(request):
    if request.method == 'POST':
      form = UploadFileForm(request.POST, request.FILES)
      if form.is_valid():
        handlezipfile(request.FILES['file'])
        return HttpResponseRedirect('/upload_successful')
    else:
      form = UploadFileForm()
    context = {'form': form}
    context.update(csrf(request))
    return render_to_response('upload.html', context)

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

