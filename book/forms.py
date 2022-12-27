from django.forms import Form, CharField, TextInput, ModelForm

from book.models import Rating


class BookSearchForm(Form):
    title = CharField(max_length=99, widget=TextInput(attrs={"class": "form-control"}), label="")


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ("star", "comment")
