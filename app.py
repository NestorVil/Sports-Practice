from flask import Flask, render_template, g, redirect, request, url_for
from database_core import DatabaseCore

app = Flask(__name__)

@app.before_request
def load_db():
    g.storage = DatabaseCore()

@app.route("/")
def index():
    sports = g.storage.get_sports()
    sports = [sport for sport in sports if sport['is_active']]
    return render_template('sport_names.html', sports=sports)

@app.route("/sports-add")
def add_sports():
    sports = g.storage.get_sports()
    sports = [sport for sport in sports if not sport['is_active']]
    return render_template('new_sport.html', sports=sports)

@app.route("/new_sport", methods=["POST"])
def new_sport():
    sport_id =  request.form.get("id")
    g.storage.add_sports(sport_id)
    return redirect('/')

@app.route("/sports/<int:sport_id>/delete", methods=["POST"])
def delete_sport(sport_id):
    g.storage.remove_sport(sport_id)
    # Potentional Flash message
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5003)