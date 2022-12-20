from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password")
        widgets = {
            "first_name": TextInput(attrs={"class": "form-control mb-3", "required": "true"}),
            "last_name": TextInput(attrs={"class": "form-control mb-3", "required": "true"}),
            "email": EmailInput(attrs={"class": "form-control mb-3", "required": "true"}),
            "username": TextInput(attrs={"class": "form-control mb-3", "required": "true"}),
            "password": PasswordInput(attrs={"class": "form-control mb-3", "required": "true"}),
        }
