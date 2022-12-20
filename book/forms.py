from django.forms import Form, CharField, TextInput


class BookSearchForm(Form):
    title = CharField(max_length=99, widget=TextInput(attrs={"class": "form-control"}), label="")
