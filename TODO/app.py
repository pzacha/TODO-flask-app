from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    done = db.Column(db.Boolean)


db.create_all()


@app.route("/")
def home():

    todo_list = Todo.query.filter_by(done=False).all()
    done_list = Todo.query.filter_by(done=True).all()

    return render_template("home.html", todo_list=todo_list, done_list=done_list)


@app.route("/add", methods=["POST"])
def add():

    todo = Todo(text=request.form["todoitem"], done=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/delete/<id>")
def delete(id):

    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/done/<id>")
def done(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    todo.done = True
    db.session.commit()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
