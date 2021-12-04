from django import forms
from .models import *

class NewBookForm(forms.ModelForm):
    class Meta:
        model = books
        fields = '__all__'
