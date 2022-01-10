from django import forms
from .data_base_alchemy.book_author_db import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NewBookForm(forms.Form):
    author_id = forms.IntegerField()
    title = forms.CharField(max_length=200)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AmountFilter(forms.Form):
    title_amount = forms.IntegerField()
