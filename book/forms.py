from django.forms import Form, CharField, TextInput, ModelForm

from book.models import Review


class BookSearchForm(Form):
    title = CharField(max_length=99, widget=TextInput(attrs={"class": "form-control"}), label="")


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "comment")
