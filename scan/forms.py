from django import forms

from .models import ScanFile


class ScanFilesForm(forms.ModelForm):

    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = ScanFile
        fields = ('photo', )


class PhotoForm(forms.Form):
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'
    }))
