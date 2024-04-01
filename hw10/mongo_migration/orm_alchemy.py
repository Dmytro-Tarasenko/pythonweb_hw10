"""SQLAlchemy ORM for the mongo_migration database."""
from os import getenv
from typing import List, Optional

from sqlalchemy import ForeignKey, create_engine, Table, Column
from sqlalchemy.orm import declarative_base, mapped_column, relationship, Mapped, sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine('sqlite:///hw10.sqlite')
# engine = create_engine('postgresql://guest:guest@localhost:5432/hw10')
DBSession = sessionmaker(bind=engine)

Base = declarative_base()


tags_quotes_association = Table(
    "tags_quotes",
    Base.metadata,
    Column("quote_id", ForeignKey("quotes.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)


class TagSQL(Base):
    """SQLAlchemy Tag Model."""
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[str] = mapped_column(nullable=False,
                                     unique=True,
                                     )
    quotes: Mapped[Optional[List["QuoteSQL"]]] = relationship(
        secondary=tags_quotes_association,
        back_populates="tags"
    )


class QuoteSQL(Base):
    """SQLAlchemy Quote Model."""
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    quote: Mapped[str] = mapped_column(nullable=False)
    author: Mapped["AuthorSQL"] = relationship()
    tags: Mapped[Optional[List["TagSQL"]]] = relationship(
        secondary=tags_quotes_association,
        back_populates="quotes"
    )


class AuthorSQL(Base):
    """SQLAlchemy Author Model."""
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(nullable=False,
                                        unique=True)
    birth_date: Mapped[Optional[str]] = mapped_column()
    birth_location: Mapped[Optional[str]] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    quotes: Mapped[Optional[List[QuoteSQL]]] = relationship()


if  __name__ == "__main__":
    Base.metadata.create_all(engine)
    author1 = AuthorSQL(fullname="John Doe",
                        birth_date="2000-01-01",
                        birth_location="USA",
                        description="A mysterious")
    author2 = AuthorSQL(fullname="Jane Doe",
                        birth_date="2002-02-02",
                        birth_location="Canada",
                        description="Cute")
    tag1 = TagSQL(tag="greeting")
    tag2 = TagSQL(tag="world")
    tag3 = TagSQL(tag="hello")

    with DBSession() as session:
        session.add(author1)
        session.add(author2)
        session.add(tag1)
        session.add(tag3)
        session.add(tag2)
        session.commit()
        author_id = session.query(AuthorSQL).filter_by(fullname="John Doe").first().id
        quote1 = QuoteSQL(author_id=author_id,
                          quote="Hello, World!",
                          tags=[tag1, tag2])
        author_id = session.query(AuthorSQL).filter_by(fullname="Jane Doe").first().id
        quote2 = QuoteSQL(author_id=author_id,
                          quote="4 None Blond!",
                          tags=[tag3, tag2])
        session.add(quote1)
        session.add(quote2)
        session.commit()
