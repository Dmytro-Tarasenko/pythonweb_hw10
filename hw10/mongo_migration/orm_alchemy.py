"""SQLAlchemy ORM for the mongo_migration database."""
from os import getenv

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, mapped_column, relationship, Mapped
from dotenv import load_dotenv

load_dotenv()

engine = create_engine('postgresql://guest:guest@localhost:5432/hw10')

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
    author: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=True)
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
    birth_date: Mapped[str] = mapped_column(nullable=True)
    birth_location: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)


if  __name__ == "__main__":
    # Base.metadata.create_all(engine)
    author1 = AuthorSQL(fullname="John Doe",
                        birth_date="2000-01-01",
                        birth_location="USA",
                        description="A mysterious")
    author1.save()
    tag1 = TagSQL(tag="greeting")
    tag2 = TagSQL(tag="world")
    tag1.save()
    tag2.save()
    quote1 = QuoteSQL(author=author1,
                      quote="Hello, World!",
                      tags=["greeting", "world"])
    quote1.save()
