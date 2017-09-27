from django import forms


class ComicUploadForm(forms.Form):
    file = forms.FileField(required=False)
