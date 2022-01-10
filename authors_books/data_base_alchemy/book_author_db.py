from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, delete, Table
from sqlalchemy.ext. declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
engine = create_engine('sqlite:///../Classed_db.sqlite3', echo=True)

Base = declarative_base()


association_table = Table('association', Base.metadata,
    Column('book_id', ForeignKey('Books.id_book'), primary_key=True),
    Column('author_id', ForeignKey('Authors.id_author'), primary_key=True)
)


class Book(Base):
    __tablename__ = 'Books'

    id_book = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author = relationship(
        "Author",
        secondary=association_table,
        backref="books")


class Author(Base):
    __tablename__ = 'Authors'

    id_author = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    book = relationship(
        "Book",
        secondary=association_table,
        backref="authors")


Base.metadata.create_all(engine)


session = sessionmaker(bind=engine)
s = session()

#print(s.query(func.count(Book.title)).filter(Book.title.contains('a')).group_by(association_table.c.author_id).all())






