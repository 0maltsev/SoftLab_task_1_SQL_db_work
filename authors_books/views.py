from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .query import *
from django.db import connection
# Create your views here.


def main(request):
    authors = conn.execute(names.select(names.c.name))
    counters = conn.execute(select([func.count(books.c.title)]).group_by(books.c.author_id))

    context = {'authors': authors, 'counters': counters}
    return render(request, 'main.html', context)

def book_list(request, pk):
    titles = conn.execute(books.select(books.c.title).where(books.c.author_id == pk))
    authors = conn.execute(names.select(names.c.name).where(names.c.id_author == pk))

    form = NewBookForm()
    form.fields['author_id'].initial = pk
    if request.method == 'POST':
        print(request.POST)
        form = NewBookForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'titles': titles, 'authors': authors, 'form': form}
    return render(request, 'book_list.html', context)
