from django.db.models import *
from .models import *


def set_authors():
    author_1 = Author(author_id=1, author='Ломоносов')
    author_1.save()
    author_2 = Author(author_id=2, author='Тютчев')
    author_2.save()
    author_3 = Author(author_id=3, author='Гоголь')
    author_3.save()
    author_4 = Author(author_id=4, author='Толстой')
    author_4.save()
    author_5 = Author(author_id=5, author='Пушкин')
    author_5.save()
    author_6 = Author(author_id=6, author='Блок')
    author_6.save()


def set_titles():
    title_1 = Title(author_id=1, title='Aa')
    title_1.save()
    title_2 = Title(author_id=1, title='Bb')
    title_2.save()
    title_3 = Title(author_id=2, title='Cc')
    title_3.save()
    title_4 = Title(author_id=3, title='Dd')
    title_4.save()
    title_5 = Title(author_id=3, title='Kk')
    title_5.save()
    title_6 = Title(author_id=4, title='Ff')
    title_6.save()
    title_7 = Title(author_id=5, title='Ee')
    title_7.save()
    title_8 = Title(author_id=5, title='Qq')
    title_8.save()
    title_9 = Title(author_id=5, title='Pp')
    title_9.save()



