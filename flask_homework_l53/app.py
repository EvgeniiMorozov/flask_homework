from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return self.title


@app.route("/")
def index():
    tasks = Tasks.query.all()
    return render_template("index.html", data=tasks)


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


if __name__ == "__main__":
    app.run(debug=True)
