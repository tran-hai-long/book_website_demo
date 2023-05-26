from django.urls import path

from . import views

app_name = "registration"
urlpatterns = [
    path("", views.RegistrationPage.as_view(), name="registration_page"),
]
