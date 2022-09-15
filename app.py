#from turtle import title
import pandas as pd
import numpy as np

from unicodedata import category
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import json
import plotly
import plotly.express as px
import plotly.graph_objects as go

from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

login_manager = LoginManager()                  #Create an Object based on LoginManager Class in order to enable Login fuctions such as load user form ID, send users
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
  
#create app
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/taskforce'  #connect to database on localhost
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
             #define variable to use modules of SQLAlchemy in this app

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    return app

