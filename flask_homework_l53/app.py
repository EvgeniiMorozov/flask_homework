from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db: SQLAlchemy = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.title


@app.route("/")
def index():
    all_tasks = {
        "current_tasks": Tasks.query.filter(Tasks.is_completed == 0).all(),
        "completed_tasks": Tasks.query.filter(Tasks.is_completed == 1).all(),
    }
    return render_template("index.html", **all_tasks)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method != "POST":
        return render_template("add_task.html")

    title = request.form["task_title"]
    description = request.form["task_description"]

    if not title or not description:
        return render_template("add_task.html", error="Ввведите данные правильно!")

    task = Tasks(title=title, description=description)

    try:
        db.session.add(task)
        db.session.commit()
        return redirect("/add")
    except:
        return "Что-то пошло не так!"


@app.route("/task_complete/<int:task_id>")
def mark_task_as_completed(task_id):
    task = Tasks.query.get(task_id)
    task.is_completed = True
    db.session.add(task)
    db.session.commit()
    return redirect("/")


@app.route("/rework/<int:task_id>")
def mark_task_as_not_completed(task_id):
    task = Tasks.query.get(task_id)
    task.is_completed = False
    db.session.add(task)
    db.session.commit()
    return redirect("/")


@app.route("/del/<int:task_id>")
def del_task(task_id):
    task = Tasks.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
