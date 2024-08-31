from django.http import HttpResponse
from django.template import loader

def scanpage(request):
    template = loader.get_template("scanner/index.html")
    return HttpResponse(template.render(None, request))
