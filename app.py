from turtle import title
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

login_manager = LoginManager()
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


# #in order to create the table named "tasks" in the database "taskforce", we need to create a model
# class Todo(db.Model):               

#     __tablename__ = 'fake_tasks'
#     #define columns of db
#     id = db.Column(db.Integer, primary_key=True)    
#     title = db.Column(db.String(100))
#     category = db.Column(db.String(50))
#     createtime = db.Column(db.DateTime())
#     completetime = db.Column(db.DateTime())
#     complete = db.Column(db.Boolean)

#     def __init__(self, title, category, createtime, completetime, complete):            #constructor
#             self.title = title;
#             self.category = category;
#             self.createtime = createtime;
#             self.completetime = completetime;
#             self.complete = complete;

# #Main Page
# @app.route('/')                         #define the Address. / means homepage
# def index():
#     #create lists of data which is needed in this page for the website
#     todo_list = db.session.query(Todo).filter_by(complete=False)      #query the db using our defined class we defined before named Todo, List will be used to display all tasks in db
#     category=[{'category': 'Select Category'},{'category': 'programming'},{'category': 'art'},{'category':'sport'}]     #define list of categories for dropdown menu
#     return render_template('index.html', category=category, todo_list=todo_list) #need to render our html template and send our created lists
#     print(todo_list)

# #define function to add tasks
# @app.route("/add", methods=["POST"]) #define address, method = POST is used to send data to a server to create/update a resource.
# def add():
#     # add new item
#     title = request.form.get("title")       #at our page we have to enter a title. ".get" takes the string from the input 
#     category = request.form.get("category")     #same priciple. get pre-defined string from dropdown menu
#     ts = datetime.now()                         #now we create a timestamp of current time to define createtime
#     ts = ts.replace(second=0, microsecond=0)    #remove seconds and microseconds
#     new_todo = Todo(title=title, category=category, createtime=ts, completetime=None, complete=False)   #create a new entry for our db which all defined columns
#     db.session.add(new_todo)            #we need session to establish all conversations with db, represents holding zone before modifying db
#     db.session.commit()                 #commit changes/modify db
#     return redirect(url_for("index"))   #redirect changes to our mainpage which will imediately show the added row in our table

# @app.route("/update/<int:todo_id>")
# def update(todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first()
#     todo.complete = not todo.complete
#     ts = datetime.now()
#     ts = ts.replace(second=0, microsecond=0)
#     todo.completetime = ts
#     db.session.commit()
#     return redirect(url_for("index"))

# @app.route("/delete/<int:todo_id>")
# def delete(todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first()
#     db.session.delete(todo)
#     db.session.commit()
#     return redirect(url_for("index"))

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/statistics')
# def statistics():
#     todo_list = Todo.query.all()
#     count = db.session.query(Todo).filter_by().count()
    
#     #import data from sql db to pandas dataframe to simplify data manipulation
#     df = pd.read_sql('SELECT * FROM fake_tasks',  db.session.bind)   #create dataframe by querying sql db and establishing session.
    
#     #create cumulative count over time grouped by categories.
#     #this enables visualizing the progress of competed task over a certain time
#     query2 = '''
#     WITH cat AS(
#             SELECT DATE(completetime) AS date, category, count(category) AS count 
#     FROM fake_tasks
#     GROUP BY date, category )
#     SELECT * , sum(count) OVER (PARTITION BY category ORDER BY date) AS count_all
#     FROM cat
#     WHERE date IS NOT NULL
#     GROUP BY date ,category, count
    
#     '''
   
#     df2 = pd.read_sql(query2,  db.session.bind) #query our db with pre-defined query to get cumulative number of tasks
    
#     #querying tasks of all categories as percentage to visualize it in pie chart later
#     query3 = '''
#     WITH cat AS(
#         SELECT category, count(category) AS count  
#         FROM fake_tasks
#         GROUP BY category)
#     SELECT *, round(100 * count / (sum(count) OVER())::numeric,2) AS percent
#     FROM cat
#     GROUP BY category ,count
    
#     '''
#     df3 = pd.read_sql(query3, db.session.bind)  #create dataframe with amount of tasks for each category unsing sql query3
   
#     tc = df.completetime - df.createtime #calculate time to complete for each task using time difference, tc = time to complete
#     tc = tc.astype('timedelta64[h]')  #transform format to display hours
#     tc = round(tc.mean(),2)
#     print(df.info())
#     df2 = df2.sort_values(by="date")
#     print(df3)
#     print(tc)
#     print(count)

#     #Graphs
#     #fig is a line chart to vizualize the cumulative amount of tasks over time of each category
#     category_list = ['programming','art','sport']

#     fig = go.Figure()
#     for k in category_list:
#         dfc = df2.loc[df2['category'] == k]
#         fig.add_trace(go.Scatter(
#             x = dfc['date'],
#             y= dfc['count_all'],
#             name = k
#         ))
#     #difine layout, distance is 5 each to the border 
#     fig.update_layout(    
#         margin=dict(l=5, r=5, t=5, b=5),
#     )
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
#     #fig2 pie-chart to vizualize allocation of tasks of each category
#     labels = df3['category'].tolist()
#     values = df3['percent'].tolist()
#     print(labels)
#     fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
#     fig2.update_layout(
#         autosize=False,
#         width=300,
#         height=150,
#         margin=dict(l=5, r=5, t=1, b=1),
#     )
#     graphJSON_2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

#     #in order to send numbers to our statistics.html, we need strings. Int, float,... wont work
#     count = str(count)
#     tc = str(tc)

#     return render_template('statistics.html', todo_list=todo_list,  graphJSON=graphJSON, graphJSON_2=graphJSON_2, count=count, tc=tc )



# if __name__ =="__main__":
#     #db.create_all()

#     app.run(debug=True)

