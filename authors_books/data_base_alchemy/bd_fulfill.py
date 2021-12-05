from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from book_author_db import *

engine = create_engine('sqlite:///../../Classed_db.sqlite3', echo=True)

# создадим сессию работы с бд
session = sessionmaker(bind=engine)
s = session()

# заполним бд значениями
s.add_all([Author(name='Ломоносов'),
           Author(name='Тютчев'),
           Author(name='Гоголь'),
           Author(name='Толстой'),
           Author(name='Пушкин'),
           Author(name='Блок'),
           Book(author_id=1, title='Aa'),
           Book(author_id=1, title='Bb'),
           Book(author_id=2, title='Cc'),
           Book(author_id=3, title='Dd'),
           Book(author_id=3, title='Kk'),
           Book(author_id=4, title='Ff'),
           Book(author_id=5, title='Ee'),
           Book(author_id=5, title='Qq'),
           Book(author_id=5, title='Pp')
        ])
s.commit()
