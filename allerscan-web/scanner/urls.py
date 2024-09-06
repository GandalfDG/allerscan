from django.urls import path

from . import views

urlpatterns = [
    path("", views.scanpage, name="scanner"),
    path("submit/", views.submitpage, name="submitted")
]