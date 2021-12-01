from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .query import *
from django.db import connection
# Create your views here.


def main(request):
    authors = Author.objects.raw("SELECT * FROM authors_books_author")
    counters = Title.objects.raw("SELECT authors_books_title.id, authors_books_title.author_id, "
                                 "COUNT(authors_books_title.title) AS total "
                                 "FROM authors_books_title GROUP BY authors_books_title.author_id")
    print(authors)
    print(counters)
    print(connection.queries)
    context = {'authors': authors, 'counters': counters}
    return render(request, 'main.html', context)

def book_list(request, pk):
    titles = Title.objects.raw("SELECT  authors_books_title.id, authors_books_title.author_id,"
                               " authors_books_title.title FROM authors_books_title " 
                               "WHERE authors_books_title.author_id = %s", [pk])

    authors = Author.objects.raw("SELECT authors_books_author.author_id, authors_books_author.author "
                                 "FROM authors_books_author WHERE authors_books_author.author_id = %s", [pk])
    print(titles)
    print(connection.queries)
    print(authors)
    print(connection.queries)
    form = NewBookForm()
    form.fields['author_id'].initial = pk
    if request.method == 'POST':
        print(request.POST)
        form = NewBookForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'titles': titles, 'authors': authors, 'form': form}
    return render(request, 'book_list.html', context)
