from .book_author_db import *
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from django.shortcuts import redirect, HttpResponse
import logging

logger = logging.getLogger(__name__)

engine = create_engine('sqlite:///../../Classed_db.sqlite3', echo=True)

# создадим сессию работы с бд
session = sessionmaker(bind=engine)
s = session()


# выводит список авторов
def author_list():
    rows = s.query(Author).all()
    result = list()
    for row in rows:
        result.append(row.name)
    return result


# выводит список книг опредленного автора
def title_list(pk):
    rows = s.query(Book).filter(Book.author_id == pk).all()
    result = list()
    for row in rows:
        result.append(row.title)
    return result


# подсчитывает количество книг определенного автора
def counter():
    rows = s.query(func.count(Book.title)).group_by(Book.author_id).all()
    result = list()
    for row in rows:
        result.append(row[0])
    return result


# выводит имя автора в заголовок его личной страницы
def author_title(pk):
    rows = s.query(Author).filter(Author.id_author == pk).all()
    result = list()
    for row in rows:
        result.append(row.name)
    return result

def add_new_book_to_db(form, request):
    if form.is_valid():
        try:
            author_id = form.cleaned_data['author_id']
            title = form.cleaned_data['title']

            s.add_all([Book(author_id=author_id, title=title)])
            s.commit()
            logger.info('client adds new book to title_list')
        except Exception as ex:
            logger.error(ex, exc_info=True)
            s.rollback()
            raise ex
        finally:
            s.close()


