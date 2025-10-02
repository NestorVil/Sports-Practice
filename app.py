from flask import Flask, render_template, g
from database_core import DatabaseCore

app = Flask(__name__)

@app.before_request
def load_db():
    g.storage = DatabaseCore()

@app.route("/")
def index():
    sports = g.storage.get_sports()
    return render_template('sport_names.html', sports=sports)

@app.route("/sports-add")
def add_sports():
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5003)