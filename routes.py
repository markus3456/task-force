from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError

#from turtle import title
import pandas as pd
import numpy as np
import sqlalchemy
import time

from unicodedata import category
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import json
import plotly
import plotly.express as px
import plotly.graph_objects as go

from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app,db,login_manager,bcrypt
from models import User, Todo, Hours
from forms import login_form,register_form




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)




@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            print(form.email.data)
            print(user)
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
        )


# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data
            
            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd).decode('utf-8'),
            )
    
            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("auth.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account"
        )

#Main Page
@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():

    if current_user.is_authenticated:    
        curr_user = current_user.id
        #curr_user = 4
        print(curr_user)
        todo_list = db.session.query(Todo).filter_by(complete=False, user_id=curr_user)      #query the db using our defined class we defined before named Todo, List will be used to display all tasks in db
        category=[{'category': 'Select Category'},{'category': 'programming'},{'category': 'art'},{'category':'sport'},{'category': 'housekeeping'},{'category': 'other'}]     #define list of categories for dropdown menu
        return render_template('index.html', category=category, todo_list=todo_list) #need to render our html template and send our created lists
    else:
        curr_user = 4
        print(curr_user)
        todo_list = db.session.query(Todo).filter_by(complete=False, user_id=curr_user)      #query the db using our defined class we defined before named Todo, List will be used to display all tasks in db
        category=[{'category': 'Select Category'},{'category': 'programming'},{'category': 'art'},{'category':'sport'}]     #define list of categories for dropdown menu
        return render_template('index.html', category=category, todo_list=todo_list) 

#define function to add tasks
@app.route("/add", methods=["POST"]) #define address, method = POST is used to send data to a server to create/update a resource.
def add():
    # add new item
    curr_user = current_user.id
    title = request.form.get("title")       #at our page we have to enter a title. ".get" takes the string from the input 
    category = request.form.get("category")     #same priciple. get pre-defined string from dropdown menu
    print(category)
    ts = datetime.now()                         #now we create a timestamp of current time to define createtime
    ts = ts.replace(second=0, microsecond=0)    #remove seconds and microseconds
    new_todo = Todo(title=title, category=category, createtime=ts, completetime=None, complete=False, user_id=curr_user)   #create a new entry for our db which all defined columns
    db.session.add(new_todo)            #we need session to establish all conversations with db, represents holding zone before modifying db
    db.session.commit()                 #commit changes/modify db
    return redirect(url_for("index"))   #redirect changes to our mainpage which will imediately show the added row in our table

#Timerfunction
# def timer():
    
#     return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    ts = datetime.now()
    ts = ts.replace(second=0, microsecond=0)
    todo.completetime = ts
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/start/<int:todo_id>")
#def hours(todo_id):
    

def start(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    #hours = Hours.query.filter_by(id=hours_id).first()
    start = datetime.now()
    start = start.replace(second=0, microsecond=0)
    new_hours = Hours(task_id=todo_id, start=start, stop=None)
    db.session.add(new_hours)
    
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/statistics')
def statistics():
    if current_user.is_authenticated: 

        engine = sqlalchemy.create_engine('postgresql://postgres:postgres@localhost:5455/mytest' )

        todo_list = db.session.query(Todo).filter_by(user_id=current_user.id)
        count = db.session.query(Todo).filter_by(user_id=current_user.id).count()
        
        #import data from sql db to pandas dataframe to simplify data manipulation
        query1 = '''SELECT * FROM fake_tasks WHERE user_id = '{}'; '''.format(current_user.id)
        df = pd.read_sql(query1,  con = engine)   #create dataframe by querying sql db and establishing session.
        
        #create cumulative count over time grouped by categories.
        #this enables visualizing the progress of competed task over a certain time
        query2 = '''
        WITH cat AS(
                SELECT DATE(completetime) AS date, category, count(category) AS count 
        FROM fake_tasks
        WHERE user_id = '{}'
        GROUP BY date, category )
        SELECT * , sum(count) OVER (PARTITION BY category ORDER BY date) AS count_all
        FROM cat
        WHERE date IS NOT NULL 
        GROUP BY date ,category, count;
        
        '''.format(current_user.id)
    
        df2 = pd.read_sql(query2,  con = engine) #query our db with pre-defined query to get cumulative number of tasks
        
        #database = 'fake_tasks'
        #querying tasks of all categories as percentage to visualize it in pie chart later
        query3 = '''
        WITH cat AS(
            SELECT category, count(category) AS count  
            FROM fake_tasks
            WHERE user_id = '{}'
            GROUP BY category)
        SELECT *, round(100 * count / (sum(count) OVER())::numeric,2) AS percent
        FROM cat
        GROUP BY category ,count;
        
        '''.format(current_user.id)

        df3 = pd.read_sql(query3, con = engine)  #create dataframe with amount of tasks for each category unsing sql query3
    
        tc = df.completetime - df.createtime #calculate time to complete for each task using time difference, tc = time to complete
        tc = tc.astype('timedelta64[h]')  #transform format to display hours
        tc = round(tc.mean(),2)
        print(df.info())
        df2 = df2.sort_values(by="date")
        print(df3)
        print(tc)
        print(count)

        #Graphs
        #fig is a line chart to vizualize the cumulative amount of tasks over time of each category

        query4 = '''SELECT category
                    FROM fake_tasks
                    WHERE user_id = '{}'
                    GROUP BY category;'''.format(current_user.id)

        df4 = pd.read_sql(query4, con = engine)
        category_list = df4['category'].tolist()
        print(df4)

        
        #category_list = ['programming','art','sport']

        fig = go.Figure()
        for k in category_list:
            dfc = df2.loc[df2['category'] == k]
            fig.add_trace(go.Scatter(
                x = dfc['date'],
                y= dfc['count_all'],
                name = k
            ))
        #difine layout, distance is 5 each to the border 
        fig.update_layout(    
            margin=dict(l=5, r=5, t=5, b=5),
        )
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        #fig2 pie-chart to vizualize allocation of tasks of each category
        labels = df3['category'].tolist()
        values = df3['percent'].tolist()
        print(labels)
        fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
        fig2.update_layout(
            autosize=False,
            width=300,
            height=150,
            margin=dict(l=5, r=5, t=1, b=1),
        )
        graphJSON_2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

        #in order to send numbers to our statistics.html, we need strings. Int, float,... wont work
        count = str(count)
        tc = str(tc)

        return render_template('statistics.html', todo_list=todo_list,  graphJSON=graphJSON, graphJSON_2=graphJSON_2, count=count, tc=tc )

    else:
        return render_template('index.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

 
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")