from flask import Flask,render_template,request
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/rufat/Desktop/flsk/todo.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    todos=Todo.query.all()
    return render_template("index.html",todos=todos)


@app.route('/add',methods=['POST'])
def addtodo():
    title=request.form.get('title')
    newTodo=Todo(title=title,completed=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/change/<string:id>')
def change(id):
    todo=Todo.query.filter_by(id=id).first()
    todo.completed=not todo.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80))
    completed=db.Column(db.Boolean)



if __name__=='__main__':
    db.create_all()
    app.run(debug=True)