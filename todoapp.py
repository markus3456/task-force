from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    category = db.Column(db.String(50))
    createtime = db.Column(db.DateTime())
    completetime = db.Column(db.DateTime())
    complete = db.Column(db.Boolean)

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
    new_todo = Todo(title=title, category=category, createtime=ts, complete=False)
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
    return render_template('statistics.html', todo_list=todo_list)

if __name__ =="__main__":
    db.create_all()
    # ts = datetime.now()
    # ts = ts.replace(second=0, microsecond=0)
    # new_todo = Todo(title="todo 1", category="programming", time=ts, complete=False)
    # db.session.add(new_todo)
    # db.session.commit()

    app.run(debug=True)