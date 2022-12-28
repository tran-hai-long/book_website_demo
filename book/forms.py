from django.forms import Form, CharField, TextInput, ModelForm, NumberInput, Textarea

from book.models import Review


class BookSearchForm(Form):
    title = CharField(max_length=99, widget=TextInput(attrs={"class": "form-control"}), label="")


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "comment")
        widgets = {
            "rating": NumberInput(attrs={"class": "form-control mb-3"}),
            "comment": Textarea(attrs={"class": "form-control mb-3"}),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields["rating"].widget.attrs["min"] = 1
        self.fields["rating"].widget.attrs["max"] = 5
