from sqlalchemy import ForeignKey
from app import db
from flask_login import UserMixin
import psycopg2
from flask_bcrypt import Bcrypt

class User(UserMixin, db.Model):
    __tablename__ = "user2"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Todo(db.Model):               

    __tablename__ = 'fake_tasks'
    #define columns of db
    id = db.Column(db.Integer, primary_key=True)    
    title = db.Column(db.String(100))
    category = db.Column(db.String(50))
    createtime = db.Column(db.DateTime())
    completetime = db.Column(db.DateTime())
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user2.id'))
    request = db.relationship("User", backref=db.backref("user2", uselist=False))

    def __init__(self, title, category, createtime, completetime, complete, user_id):            #constructor
            self.title = title;
            self.category = category;
            self.createtime = createtime;
            self.completetime = completetime;
            self.complete = complete;
            self.user_id = user_id;
