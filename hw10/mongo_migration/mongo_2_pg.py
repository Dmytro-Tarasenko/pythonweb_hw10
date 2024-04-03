"""Migration script from MongoDB to PostgreSQL"""
from sqlalchemy.orm import sessionmaker
from orm_alchemy import TagSQL, AuthorSQL, QuoteSQL, Base, engine

from odm_mongo import AuthorMongo, QuoteMongo


def is_tag_in(tag: str) -> bool:
    with pg_session() as session:
        res = session.query(TagSQL).filter_by(tag=tag).first()

    return bool(res)


def is_author_in(author_name: str) -> bool:
    with pg_session() as session:
        res = session.query(AuthorSQL).filter_by(fullname=author_name).first()

    return bool(res)


def is_quote_in(quote_text: str) -> bool:
    with pg_session() as session:
        res = session.query(QuoteSQL).filter_by(quote=quote_text).first()

    return bool(res)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(engine)
    for quote_mongo in QuoteMongo.objects:
        author_mongo: AuthorMongo = quote_mongo.author
        tags_mongo = quote_mongo.tags
        tags = [TagSQL(tag=tag_) for tag_ in tags_mongo]
        author = AuthorSQL(fullname=author_mongo.fullname,
                           born_date=author_mongo.born_date,
                           born_location=author_mongo.born_location,
                           description=author_mongo.description)
        quote = QuoteSQL(quote=quote_mongo.quote,
                         author=author,
                         tags=tags)
        with DBSession() as session:
            session.add(quote)
            session.commit()
            print("Quote:", quote.author.fullname, quote.tags, "added.")
