from django import forms
from .data_base_alchemy.book_author_db import *

class NewBookForm(forms.Form):
    author_id = forms.IntegerField()
    title = forms.CharField(max_length=200)