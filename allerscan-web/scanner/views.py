from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .forms import ImageUploadForm

def scanpage(request):
    
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.files)
        
    else:
        form = ImageUploadForm()
    
    return render(request, "scanner/index.html", {"form": form})