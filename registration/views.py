from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from registration.forms import RegistrationForm


def registration_page(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                form.cleaned_data["username"],
                form.cleaned_data["email"],
                form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            return HttpResponseRedirect(reverse("book_list"))
        else:
            return HttpResponse("User creation error.")
    else:
        context = {"form": RegistrationForm()}
        return render(request, "registration/registration.html", context)
