from django import forms
from .models import *

class NewBookForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = '__all__'
