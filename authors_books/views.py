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

    try:
        book_id_counter = func.count(association_table.c.book_id)

        # базовый запрос для всех дальнейших фильтраций
        sql_filtered_rows = s.query(Book, association_table, Author, book_id_counter).join(
            Book, Book.id_book == association_table.c.book_id).join(Author, Author.id_author == association_table.c.author_id)

        if request.method == 'GET':
            try:
                sql_filtered_rows = sql_filtered_rows.group_by(association_table.c.author_id)
                logger.info('client requests main screen')
            except Exception as ex:
                logger.error(ex, exc_info=True)
                s.rollback()
                raise ex
            finally:
                s.close()

        # фильтрация
        filtering = Filter()

        if request.method == 'POST':

            filtering = Filter(request.POST)
            try:
                if filtering.is_valid():

                    amount = filtering.cleaned_data['title_amount']
                    substring = filtering.cleaned_data.get('substring')

                    if substring == '' and amount is not None:
                        try:
                            sql_filtered_rows = sql_filtered_rows.group_by(
                                association_table.c.author_id).having(book_id_counter >= amount)
                        except Exception as ex:
                            logger.error(ex, exc_info=True)
                            s.rollback()
                            raise ex
                        finally:
                            s.close()

                    elif amount is None and substring != '':
                        try:
                            sql_filtered_rows = sql_filtered_rows.filter(Book.title.contains(substring)).group_by(
                                association_table.c.author_id)
                        except Exception as ex:
                            logger.error(ex, exc_info=True)
                            s.rollback()
                            raise ex
                        finally:
                            s.close()

                    elif amount is None and substring == '':
                        try:
                            sql_filtered_rows = sql_filtered_rows.group_by(association_table.c.author_id)
                        except Exception as ex:
                            logger.error(ex, exc_info=True)
                            s.rollback()
                            raise ex
                        finally:
                            s.close()

                    else:
                        try:
                            sql_filtered_rows = sql_filtered_rows.filter(Book.title.contains(substring)).group_by(
                                association_table.c.author_id).having(book_id_counter >= amount)
                        except Exception as ex:
                            logger.error(ex, exc_info=True)
                            s.rollback()
                            raise ex
                        finally:
                            s.close()

            except:
                return HttpResponse(status=500, content="Internal Server Error")


        filtered_rows = sql_filtered_rows.all()

        author_and_counter = dict()
        result = list()
        for row in filtered_rows:
            author_and_counter = {'id_author': row[3].id_author, 'name': row[3].name, 'counter': row[4]}
            result.append(author_and_counter)
        print(result)




        # authors = list()
        # counters = list()
        # for row in filtered_rows:
        #     authors.append(row[3])
        #     counters.append(row[4])
        # context = {'authors': authors, 'counters': counters, 'filtering': filtering}


        context = {'result': result, 'filtering': filtering}
        return render(request, 'main.html', context)

    except:
        return HttpResponse(status=500, content="Internal Server Error")



def book_list(request, pk):

    session = sessionmaker(bind=engine)
    s = session()
    try:
        book_ids = s.query(association_table.c.book_id).filter(association_table.c.author_id == pk).all()
        titles = list()
        for element in book_ids:
            titles.append(s.query(Book).filter(Book.id_book == element[0]).all()[0])

        authors_query = s.query(Author)
        authors = authors_query.filter(Author.id_author == pk).all()
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
                    writer = authors_query.filter(Author.id_author == author_id).all()[0]
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
