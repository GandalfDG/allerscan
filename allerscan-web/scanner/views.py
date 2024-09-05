from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .forms import ImageUploadForm

def scanpage(request):
    
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_field = form.cleaned_data["image"]
            print(image_field.image)
        
    else:
        form = ImageUploadForm()
    
    return render(request, "scanner/index.html", {"form": form})