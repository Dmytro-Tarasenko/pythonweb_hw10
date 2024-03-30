"""MongoDB ODM Models"""
from os import getenv
from mongoengine import (connect,
                         Document,
                         StringField,
                         ReferenceField,
                         ListField)

from dotenv import load_dotenv

load_dotenv()

ATLAS_HOST = getenv('ATLAS_HOST')
if ATLAS_HOST is None:
    ATLAS_HOST = 'mongodb+localhost//'
ATLAS_PARAMS = getenv('ATLAS_PARAMS')
DB_NAME = "pythonweb_hw08 "

connect(DB_NAME, host=ATLAS_HOST + ATLAS_PARAMS)


class AuthorMongo(Document):
    """MongoDB Author Document"""
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()
    meta = {'collection': 'authors'}


class QuoteMongo(Document):
    """MongoDB Quote Document"""
    author = ReferenceField(AuthorMongo, required=True, dbref=True)
    tags = ListField(StringField())
    quote = StringField()
    meta = {'collection': 'quotes'}
