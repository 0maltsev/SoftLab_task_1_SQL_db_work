from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.ext. declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///../../Classed_db.sqlite3', echo=True)

Base = declarative_base()


class Book(Base):
    __tablename__ = 'Books'

    id_book = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey("Authors.id_author"))
    author = relationship("Author")


class Author(Base):
    __tablename__ = 'Authors'

    id_author = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    book = relationship("Book")


Base.metadata.create_all(engine)
