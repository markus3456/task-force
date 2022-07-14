import pandas
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from unicodedata import category
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost:5432/taskforce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()
db.session.commit()

admin = User('admin', 'admin@example.com')
guest = User('guest', 'guest@example.com')
db.session.add(admin)
db.session.add(guest)
db.session.commit()
users = User.query.all()
print(users)







# app = Flask(__name__)

# Base = declarative_base()
 
# # DEFINE THE ENGINE (CONNECTION OBJECT)
# engine = db.create_engine('postgresql+psycopg2://postgres:admin@localhost:5432/taskforce', pool_recycle=3600)
# db.SQLAlchemy(app) 
# # CREATE THE TABLE MODEL TO USE IT FOR QUERYING
# # class Students(Base):
 
# #     __tablename__ = 'students'
 
# #     first_name = db.Column(db.String(50),
# #                            primary_key=True)
# #     last_name  = db.Column(db.String(50),
# #                            primary_key=True)
# #     course     = db.Column(db.String(50))
# #     score      = db.Column(db.Float)

# class Todo(Base):

#     __tablename__ = 'todo'

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100))
#     category = db.Column(db.String(50))
#     createtime = db.Column(db.DateTime())
#     completetime = db.Column(db.DateTime())
#     complete = db.Column(db.Boolean)

# # CREATE TABLE
# db.create_all()
# ts = datetime.now()
# ts = ts.replace(second=0, microsecond=0)
# new_todo = Todo(title="todo 1", category="programming", createtime=ts, complete=False)
# db.session.add(new_todo)
# db.session.commit()

# # SQLAlCHEMY ORM QUERY TO FETCH ALL RECORDS
# df = pandas.read_sql_query(
#     sql = db.select([Todo.id,
#                      Todo.title,
#                      Todo.category,
#                      Todo.createtime,
#                      Todo.completetime,
#                      Todo.complete]),
#     con = engine
# )
 
# print("Type:", type(df))
# print()
# print(df)