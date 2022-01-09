from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from book_author_db import *

engine = create_engine('sqlite:///../Classed_db.sqlite3', echo=True)

# создадим сессию работы с бд
session = sessionmaker(bind=engine)
s = session()

writer_1 = Author(name='Ломоносов')
writer_2 = Author(name='Тютчев')
book_1 = Book(title='Aa')
book_2 = Book(title='Bb')
writer_1.book.append(book_1)
writer_1.book.append(book_2)
writer_2.book.append(book_1)
writer_2.book.append(book_2)

# заполним бд значениями
s.add_all([writer_1, writer_2, book_1, book_2])
s.commit()
