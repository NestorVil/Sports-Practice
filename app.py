from flask import Flask, render_template, g, redirect, request, url_for, abort
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
    return redirect(url_for("index"))

@app.route("/sports/<int:sport_id>/")
def team(sport_id):
    sports = g.storage.get_sports() 
    if sport_id not in (sport['id'] for sport in sports if sport['is_active']):
        return abort(404)

    teams = g.storage.get_teams(sport_id)
    return render_template('team_names.html', teams=teams, sport_id=sport_id)

@app.route("/sports/<int:sport_id>/add_team")
def add_new_team(sport_id):
    return render_template("new_team.html", sport_id=sport_id)

@app.route("/sports/<int:sport_id>/new_team", methods=["POST"])
def create_team(sport_id):
    team_name = request.form.get("team_name", "").strip()
    
    if not team_name:
        return abort(404)

    g.storage.add_team(team_name, sport_id)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5003)