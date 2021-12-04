from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey, func

# зададим бд

meta = MetaData()

names = Table('Authors', meta,
              Column('id_author', Integer, primary_key=True),
              Column('name', String(250), nullable=False),
)

books = Table('Books', meta,
              Column('id_book', Integer, primary_key=True),
              Column('title', String(250), nullable=False),
              Column('author_id', Integer, ForeignKey("Authors.id_author"))
)

# подключение к бд
engine = create_engine('sqlite:///SoftLab.db', echo=True)
meta.create_all(engine)

conn = engine.connect()

# заполним бд
author_1 = names.insert().values(name='Ломоносов')
conn.execute(author_1)
author_2 = names.insert().values(name='Тютчев')
conn.execute(author_2)
author_3 = names.insert().values(name='Гоголь')
conn.execute(author_3)
author_4 = names.insert().values(name='Толстой')
conn.execute(author_4)
author_5 = names.insert().values(name='Пушкин')
conn.execute(author_5)
author_6 = names.insert().values(name='Блок')
conn.execute(author_6)

title_1 = books.insert().values(author_id=1, title='Aa')
conn.execute(title_1)
title_2 = books.insert().values(author_id=1, title='Bb')
conn.execute(title_2)
title_3 = books.insert().values(author_id=2, title='Cc')
conn.execute(title_3)
title_4 = books.insert().values(author_id=3, title='Dd')
conn.execute(title_4)
title_5 = books.insert().values(author_id=3, title='Kk')
conn.execute(title_5)
title_6 = books.insert().values(author_id=4, title='Ff')
conn.execute(title_6)
title_7 = books.insert().values(author_id=5, title='Ee')
conn.execute(title_7)
title_8 = books.insert().values(author_id=5, title='Qq')
conn.execute(title_8)
title_9 = books.insert().values(author_id=5, title='Pp')
conn.execute(title_9)



result = select([func.count(books.c.title)]).group_by(books.c.author_id)

runner_1 = conn.execute(result)
for row in runner_1:
    print(row)




titles = books.select(books.c.title).where(books.c.author_id == 1)
runner_2 = conn.execute(titles)
for row in runner_2:
    print(row)

writers = names.select(names.c.name).where(names.c.id_author == 1)
runner_3 = conn.execute(writers)



