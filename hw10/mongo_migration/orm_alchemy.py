"""SQLAlchemy ORM for the mongo_migration database."""
from os import getenv

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, mapped_column, relationship, Mapped
from dotenv import load_dotenv

load_dotenv()

engine = create_engine()

Base = declarative_base()


class TagSQL(Base):
    """SQLAlchemy Tag Model."""
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[str] = mapped_column(nullable=False,
                                    unique=True,
                                     )
    quotes: Mapped[list["QuoteSQL"]] = relationship(
        back_populates="tags"
    )


class QuoteSQL(Base):
    """SQLAlchemy Quote Model."""
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    quote: Mapped[str] = mapped_column(nullable=False)
    tags: Mapped[list["TagSQL"]] = relationship(
        back_populates="quotes"
    )


class AuthorSQL(Base):
    """SQLAlchemy Author Model."""
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(nullable=False,
                                         unique=True)
    birth_date: Mapped[str] = mapped_column()
    birth_location: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
