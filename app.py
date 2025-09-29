# NFL APP in FLASK
from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# A dictionary of all 32 NFL teams with their IDs
NFL_TEAMS = {
	"arizona cardinals": "134960",
	"atlanta falcons": "134944",
	"baltimore ravens": "134922",
	"buffalo bills": "134921",
	"carolina panthers": "134952",
	"chicago bears": "134918",
	"cincinnati bengals": "134923",
	"cleveland browns": "134924",
	"dallas cowboys": "134925",
	"denver broncos": "134926",
	"detroit lions": "134927",
	"green bay packers": "134928",
	"houston texans": "134929",
	"indianapolis colts": "134930",
	"jacksonville jaguars": "134931",
	"kansas city chiefs": "134920",
	"las vegas raiders": "134933",
	"los angeles chargers": "134934",
	"los angeles rams": "134935",
	"miami dolphins": "134936",
	"minnesota vikings": "134937",
	"new england patriots": "134917",
	"new orleans saints": "134938",
	"new york giants": "134939",
	"new york jets": "134940",
	"philadelphia eagles": "134919",
	"pittsburgh steelers": "134941",
	"san francisco 49ers": "134942",
	"seattle seahawks": "134943",
	"tampa bay buccaneers": "134945",
	"tennessee titans": "134946",
	"washington commanders": "134947"
}

TEAM_DISPLAY_NAMES = {
	"arizona cardinals": "Arizona Cardinals",
	"atlanta falcons": "Atlanta Falcons",
	"baltimore ravens": "Baltimore Ravens",
	"buffalo bills": "Buffalo Bills",
	"carolina panthers": "Carolina Panthers",
	"chicago bears": "Chicago Bears",
	"cincinnati bengals": "Cincinnati Bengals",
	"cleveland browns": "Cleveland Browns",
	"dallas cowboys": "Dallas Cowboys",
	"denver broncos": "Denver Broncos",
	"detroit lions": "Detroit Lions",
	"green bay packers": "Green Bay Packers",
	"houston texans": "Houston Texans",
	"indianapolis colts": "Indianapolis Colts",
	"jacksonville jaguars": "Jacksonville Jaguars",
	"kansas city chiefs": "Kansas City Chiefs",
	"las vegas raiders": "Las Vegas Raiders",
	"los angeles chargers": "Los Angeles Chargers",
	"los angeles rams": "Los Angeles Rams",
	"miami dolphins": "Miami Dolphins",
	"minnesota vikings": "Minnesota Vikings",
	"new england patriots": "New England Patriots",
	"new orleans saints": "New Orleans Saints",
	"new york giants": "New York Giants",
	"new york jets": "New York Jets",
	"philadelphia eagles": "Philadelphia Eagles",
	"pittsburgh steelers": "Pittsburgh Steelers",
	"san francisco 49ers": "San Francisco 49ers",
	"seattle seahawks": "Seattle Seahawks",
	"tampa bay buccaneers": "Tampa Bay Buccaneers",
	"tennessee titans": "Tennessee Titans",
	"washington commanders": "Washington Commanders"
}

POPULAR_PLAYERS = {
	"patrick mahomes": "Patrick Mahomes",
	"tom brady": "Tom Brady",
	"aaron rodgers": "Aaron Rodgers",
	"josh allen": "Josh Allen",
	"joe burrow": "Joe Burrow",
	"justin jefferson": "Justin Jefferson",
	"travis kelce": "Travis Kelce",
	"christian mccaffrey": "Christian McCaffrey",
	"tyreek hill": "Tyreek Hill",
	"myles garrett": "Myles Garrett"
}

@app.route("/")
def index():
	return render_template("index.html", teams=TEAM_DISPLAY_NAMES, popular_players=POPULAR_PLAYERS)

@app.route("/games")
def games():
	url = "https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id=134922"
	response = requests.get(url)
	data = response.json()
	games = data.get("results", []) # list of matches
	return render_template("games.html", games=games, team_name="Baltimore Ravens")

@app.route("/search", methods=["GET", "POST"])
def search_team():
	if request.method == "POST":
		team_name = request.form.get("team_name", "").lower().strip()
		
		if team_name in NFL_TEAMS:
			team_id = NFL_TEAMS[team_name]
			display_name = TEAM_DISPLAY_NAMES[team_name]

			url = f"https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id={team_id}"
			response = requests.get(url)
			data = response.json()

			games = data.get("results", [])
			return render_template("team_results.html", games=games, team_name=display_name, search_query=team_name)
		else:
			return render_template("search.html", error="Team not found. Try full team name (e.g., 'dallas cowboys')", 
						  teams=TEAM_DISPLAY_NAMES)
	return render_template("search.html", teams=TEAM_DISPLAY_NAMES)

@app.route("/team/<team_key>")
def team_games(team_key):
	if team_key in NFL_TEAMS:
		team_id = NFL_TEAMS[team_key]
		display_name = TEAM_DISPLAY_NAMES[team_key]

		url = f"https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id={team_id}"
		response = requests.get(url)
		data = response.json()

		games = data.get("results", [])
		return render_template("team_results.html", games=games, team_name=display_name, search_query=team_key)
	
	return render_template("search.html", error="Team not found", teams=TEAM_DISPLAY_NAMES)


@app.route("/players", methods=["GET", "POST"])
def search_players():
	if request.method == "POST":
		player_name = request.form.get("player_name", "").strip()
		
		if player_name:
			# seek the player in API
			url = f"https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={player_name}"
			response = requests.get(url)
			data = response.json()

			players = data.get("player", [])

			# filter only NFL players
			nfl_players = [p for p in players if p.get("strSport") == "American Football"]
			return render_template("player_results.html", players=nfl_players, search_query=player_name, results_count=len(nfl_players))
		else:
			return render_template("player_search.html", error="Please enter a player name", popular_players=POPULAR_PLAYERS)
	
	return render_template("player_search.html", popular_players=POPULAR_PLAYERS)

# player details page
@app.route("/player/<player_id>")
def player_detail(player_id):
	# download player details
	url = f"https://www.thesportsdb.com/api/v1/json/3/lookupplayer.php?id={player_id}"
	response = requests.get(url)
	data = response.json()

	player = data.get("players", [{}])[0] if data.get("players") else {}

	# Download career stats (if available)
	stats_url = f"https://www.thesportsdb.com/api/v1/json/3/lookupplayer.php?id={player_id}"

	return render_template("player_detail.html", player=player)


if __name__ == "__main__":
	app.run(debug=True)
