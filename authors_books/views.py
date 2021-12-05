from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .query import *
from django.db import connection
from .data_base_alchemy.book_author_db import *
from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker
# Create your views here.

engine = create_engine('sqlite:///../../Classed_db.sqlite3', echo=True)

# создадим сессию работы с бд
session = sessionmaker(bind=engine)
s = session()

def main(request):
    authors = s.query(Author).all()
    counters = s.query(func.count(Book.title)).group_by(Book.author_id).all()
    context = {'authors': authors, 'counters': counters}
    return render(request, 'main.html', context)

def book_list(request, pk):
    titles = s.query(Book).filter(Book.author_id == pk).all()
    authors = s.query(Author).filter(Author.id_author == pk).all()



    context = {'titles': titles, 'authors': authors}
    return render(request, 'book_list.html', context)
