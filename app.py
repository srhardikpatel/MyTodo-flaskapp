import os
from typing import Optional
from flask import Flask, render_template, request, redirect
from sqlmodel import Field, SQLModel, create_engine, Session, select, Column, DateTime, func
from datetime import datetime

app = Flask(__name__)

MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'default_user')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'default_user')
MYSQL_DB = os.environ.get('MYSQL_DB', 'default_db')

class Todo(SQLModel, table=True):
    sno: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    data_created: Optional[datetime] = Field(sa_column=Column(DateTime(), server_default=func.now()))

mysql_url = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
engine = create_engine(mysql_url)

def init_db():
        SQLModel.metadata.create_all(engine)

@app.route('/', methods=['GET', 'POST'])
def my_todo():
    with Session(engine) as session:

      if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, description=desc)
        session.add(todo)
        session.commit()

      allTodo = session.exec(select(Todo)).all()
    session.close()
    return render_template('index.html', allTodo=allTodo)

@app.route('flask/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    with Session(engine) as session:

        if request.method=='POST':
          title = request.form['title']
          desc = request.form['desc']
          todo = session.exec(select(Todo).where(Todo.sno == sno)).first()
          todo.title = title
          todo.description = desc
          session.add(todo)
          session.commit()
          return redirect("/flask")

        todo = todo = session.exec(select(Todo).where(Todo.sno == sno)).first()
    session.close()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    with Session(engine) as session:

        todo = session.exec(select(Todo).where(Todo.sno == sno)).first()
        session.delete(todo)
        session.commit()
        session.close()
    return redirect("/")


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
