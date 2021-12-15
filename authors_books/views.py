import logging
from .data_base_alchemy.return_functions import add_new_book_to_db
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
from .forms import *
from .query import *
from django.db import connection
from .data_base_alchemy.book_author_db import *
from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker
# Create your views here.

logger = logging.getLogger(__name__)

engine = create_engine('sqlite:///../../Classed_db.sqlite3', echo=True)


def main(request):

    session = sessionmaker(bind=engine)
    s = session()

    try:
        authors = s.query(Author).all()
        rows = s.query(func.count(Book.title)).group_by(Book.author_id).all()
        counters = list()
        for row in rows:
            counters.append(row[0])
        logger.info('client requests main screen')
    except Exception as ex:
        problem_check = 1
        logger.error(ex, exc_info=True)
        s.rollback()
        return HttpResponse(status=500, content="Internal Server Error")
    finally:
        s.close()

    context = {'authors': authors, 'counters': counters}
    return render(request, 'main.html', context)



def book_list(request, pk):

    session = sessionmaker(bind=engine)
    s = session()
    try:
        titles = s.query(Book).filter(Book.author_id == pk).all()
        authors = s.query(Author).filter(Author.id_author == pk).all()
        logger.info('client requests title_list')
    except Exception as ex:
        logger.error(ex, exc_info=True)
        s.rollback()
        return HttpResponse(status=500, content="Internal Server Error")
    finally:
        s.close()

    form = NewBookForm()
    form.fields['author_id'].initial = pk
    if request.method == 'POST':
        form = NewBookForm(request.POST)
        return add_new_book_to_db(form, request)

    context = {'titles': titles, 'authors': authors, 'form': form}
    return render(request, 'book_list.html', context)

