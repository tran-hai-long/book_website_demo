from django.urls import path

from . import views

urlpatterns = [
    path("", views.RegistrationPage.as_view(), name="registration_page"),
]
