from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.password_validation import validate_password

from book.models import ShoppingCart
from registration.forms import RegistrationForm


def registration_page(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
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
            try:
                validate_password(form.cleaned_data["password"])
            except ValidationError as e:
                context = {"form": RegistrationForm(), "error": str(e)}
                return render(request, "registration/registration.html", context)
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
    else:
        context = {"form": RegistrationForm()}
        return render(request, "registration/registration.html", context)
