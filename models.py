import os
from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
  DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
  DATABASE = SqliteDatabase('dogs.sqlite')


class User(UserMixin, Model):
  username=CharField(unique=True)
  password=CharField()

  class Meta:
    database = DATABASE

class User_pref(Model):
  name=CharField()
  owner=ForeignKeyField(User, backref='user_prefs')
  clean_pref=IntegerField()
  big_pref=IntegerField()
  fenced_pref=IntegerField()
  busy_pref=IntegerField()
  note=CharField()

  class Meta:
    database = DATABASE

class Dog(Model):
  name=CharField()
  owner=ForeignKeyField(User, backref='dogs')
  breed=CharField()
  created_at=DateTimeField(default=datetime.datetime.now)
  image=CharField()

  class Meta: 
    database = DATABASE

class Park(Model):
  name=CharField()
  owner=ForeignKeyField(User, backref='parks')
  location=CharField()
  clean=IntegerField()
  big=IntegerField()
  fenced=IntegerField()
  busy=IntegerField()
  image=CharField()
  # current_time=DateTimeField(default=datetime.datetime.now)

  class Meta: 
    database = DATABASE

def initialize():
  DATABASE.connect()

  DATABASE.create_tables([User, User_pref, Dog, Park], safe=True)
  print("CONNECTED to DB and CREATED (User, User_pref, Dog, Park) TABLES if they weren't already there")

  DATABASE.close()






