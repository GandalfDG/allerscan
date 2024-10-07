from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.conf import settings

import logging

from PIL import Image
import os

from .forms import ImageUploadForm
from . import readapi
from .allergenmatcher import AllergenMatcher

logger = logging.getLogger(__name__)

allergy_matcher = AllergenMatcher("scanner/allergens.yaml")

def scanpage(request):
    
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_field = form.cleaned_data["image"]
            
            with Image.open(image_field) as image:
                upload_filename = f"upload.{image.format}"
                upload_url = settings.MEDIA_URL + upload_filename
                try:
                    image.save(os.path.join(settings.MEDIA_ROOT, upload_filename), format=image.format)

                    api_response = None
                    if not os.getenv("DJANGO_MEDIA_ROOT"):
                        api_response = readapi.read_api_request("https://allergy.jack-case.pro/media/upload.jpg")
                    else: 
                        api_response = readapi.read_api_request(upload_url)
                    
                    full_text = api_response.json()["readResult"]["content"]
                    matching_allergens = allergy_matcher.match_allergens(full_text)
                    print(matching_allergens)



                    return HttpResponse(f"matches: {matching_allergens}")
                except OSError as err:
                    logger.error("Couldn't save uploaded image", exc_info=err)
                

        
    else:
        form = ImageUploadForm()
    
    return render(request, "scanner/index.html", {"form": form})
