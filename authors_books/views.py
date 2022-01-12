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
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .utils import RESP_MSG_INTERNAL_ERROR
from django.contrib.auth.decorators import login_required
# Create your views here.

logger = logging.getLogger(__name__)

engine = create_engine('sqlite:///../Classed_db.sqlite3', echo=True)


def main(request):

    session = sessionmaker(bind=engine)
    s = session()

    idents = list()
    writers = list()
    filtered_counters = list()
    filtered_authors = list()
    try:
        authors = s.query(Author).all()
        rows = s.query(func.count(association_table.c.book_id)).group_by(association_table.c.author_id).all()
        counters = list()
        for row in rows:
            counters.append(row[0])
        logger.info('client requests main screen')
    except Exception as ex:

        logger.error(ex, exc_info=True)
        s.rollback()
        return HttpResponse(status=500, content=RESP_MSG_INTERNAL_ERROR)
    finally:
        s.close()

    amount_filtering = AmountFilter()
    substring_filtering = SubstringFilter()
    if request.method == 'POST':
        if "amount" in request.POST:
            amount_filtering = AmountFilter(request.POST)

            if amount_filtering.is_valid():
                amount = amount_filtering.cleaned_data['title_amount']
                writers_idents = s.query(association_table.c.author_id).group_by(
                    association_table.c.author_id).having(func.count(association_table.c.book_id) >= amount)
                for element in writers_idents:
                    idents.append(element[0])
                for element in idents:
                    writers.append(s.query(Author.name).filter(Author.id_author == element).all()[0][0])
                s.close()

            context = {'writers': writers}
            return render(request, 'filtered_authors.html', context)

        else:
            substring_filtering = SubstringFilter(request.POST)

            if substring_filtering.is_valid():
                substring = substring_filtering.cleaned_data.get('substring')
                filtered_authors = s.query(Author).all()
                filtered_rows = s.query(Book, association_table, func.count(association_table.c.book_id)).join(Book, Book.id_book == association_table.c.book_id).filter(Book.title.contains(substring)).group_by(association_table.c.author_id).all()
                for row in filtered_rows:
                    filtered_counters.append(row[3])
                s.close()
                print(substring)

            context = {'authors': filtered_authors, 'counters': filtered_counters, 'amount_filtering': amount_filtering,
                       'substring_filtering': substring_filtering}
            return render(request, 'main.html', context)


    context = {'authors': authors, 'counters': counters, 'amount_filtering': amount_filtering, 'substring_filtering': substring_filtering}
    return render(request, 'main.html', context)



def book_list(request, pk):

    session = sessionmaker(bind=engine)
    s = session()
    try:
        book_ids = s.query(association_table.c.book_id).filter(association_table.c.author_id == pk).all()
        titles = list()
        for element in book_ids:
            titles.append(s.query(Book).filter(Book.id_book == element[0]).all()[0])

        authors = s.query(Author).filter(Author.id_author == pk).all()
        logger.info('client requests title_list')
    except Exception as ex:
        logger.error(ex, exc_info=True)
        s.rollback()
        return HttpResponse(status=500, content=RESP_MSG_INTERNAL_ERROR)
    finally:
        s.close()

    form = NewBookForm()
    form.fields['author_id'].initial = pk
    if request.method == 'POST':
        form = NewBookForm(request.POST)
        try:
            if form.is_valid():
                try:
                    author_id = form.cleaned_data['author_id']
                    title = form.cleaned_data['title']
                    writer = s.query(Author).filter(Author.id_author == author_id).all()[0]
                    new_book = Book(title=title)
                    writer.book.append(new_book)
                    s.add_all([new_book])
                    s.commit()
                    logger.info('client adds new book to title_list')
                except Exception as ex:
                    logger.error(ex, exc_info=True)
                    s.rollback()
                    raise ex
                finally:
                    s.close()
            return redirect(request.META['HTTP_REFERER'])
        except:
            return HttpResponse(status=500, content="Internal Server Error")

    context = {'titles': titles, 'authors': authors, 'form': form}
    return render(request, 'book_list.html', context)










def register_page(request):
    if request.user.is_authenticated:
        return redirect('author_list')
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'User {username} was created')
                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('author_list')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('author_list')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')
