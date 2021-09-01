from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Tasks(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.title


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_task():
    return render_template("add_task.html")


if __name__ == "__main__":
    app.run(debug=True)
