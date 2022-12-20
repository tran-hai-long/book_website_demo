from django.urls import path

from . import views

urlpatterns = [
    path("", views.registration_page, name="registration_page"),
]
