from peewee import *
from flask_login import UserMixin
import os

from playhouse.db_url import connect

# work on heroku
# DATABASE = connect(os.environ.get('DATABASE_URL'))

# work locally
DATABASE = SqliteDatabase("bookshare.sqlite")

class User(UserMixin, Model):
    username = CharField()
    password = CharField()
    email = CharField()
    photo = CharField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    print("TABLE CREATED")
    DATABASE.close()