from turtle import title
import pandas as pd

from unicodedata import category
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/taskforce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    category = db.Column(db.String(50))
    createtime = db.Column(db.DateTime())
    completetime = db.Column(db.DateTime())
    complete = db.Column(db.Boolean)

    def __init__(self, title, category, createtime, completetime, complete):            #constructor
            self.title = title;
            self.category = category;
            self.createtime = createtime;
            self.completetime = completetime;
            self.complete = complete;

@app.route('/')
def index():
    todo_list = Todo.query.all()
    category=[{'category': 'Select Category'},{'category': 'programming'},{'category': 'art'},{'category':'sport'}]
    return render_template('index.html', category=category, todo_list=todo_list)
    print(todo_list)

@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    category = request.form.get("category")
    ts = datetime.now()
    ts = ts.replace(second=0, microsecond=0)
    new_todo = Todo(title=title, category=category, createtime=ts, completetime=None, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/statistics')
def statistics():
    todo_list = Todo.query.all()
    q = Todo.query.filter_by(category='programming').first()
    print(q)

    q2 = db.session.query(Todo).filter_by(category='programming').count()
    print(q2)

    q3 = db.session.query(Todo).all()
    print(q3)
    df = pd.read_sql('SELECT * FROM tasks',  db.session.bind)
    query = ' category FROM tasks WHERE complete = true'
    
    query4 = '''
    SELECT DATE(completetime) AS date, category, count(category) AS count 
    FROM tasks
    GROUP BY date, category

    '''

    query2 = '''
    WITH cat AS(
            SELECT DATE(completetime) AS date, category, count(category) AS count 
    FROM tasks
    GROUP BY date, category )
    SELECT * , sum(count) OVER (PARTITION BY category ORDER BY count) AS count_all
    FROM cat
    GROUP BY date ,category, count
    
    '''
   

    df2 = pd.read_sql(query2,  db.session.bind)
    print(df.info())
    print(df2)
    b = df.completetime - df.createtime
    b = b.astype('timedelta64[h]')
    print(b)

    return render_template('statistics.html', todo_list=todo_list)

if __name__ =="__main__":
    #db.create_all()

    app.run(debug=True)