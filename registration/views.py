from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.password_validation import validate_password
from django.views import View

from book.models import ShoppingCart
from registration.forms import RegistrationForm


class RegistrationPage(View):
    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        # Check for duplicate username
        username = form.data["username"]
        username_not_taken = False
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            username_not_taken = True
        if not username_not_taken:
            context = {"form": RegistrationForm(), "error": "This username is already taken."}
            return render(request, "registration/registration.html", context)
        elif form.is_valid():
            # If password does not meets requirements, display the error message
            try:
                validate_password(form.cleaned_data["password"])
            except ValidationError as e:
                context = {"form": RegistrationForm(), "error": str(e)}
                return render(request, "registration/registration.html", context)
            # If input is valid, create a new user and their ShoppingCart object
            user = User.objects.create_user(
                form.cleaned_data["username"],
                form.cleaned_data["email"],
                form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            ShoppingCart.objects.create(user_id=user.pk)
            return HttpResponseRedirect(reverse("book_list"))
        else:
            return HttpResponse("User creation error.")

    def get(self, request, *args, **kwargs):
        context = {"form": RegistrationForm()}
        return render(request, "registration/registration.html", context)
