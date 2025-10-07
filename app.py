# Nfl App with ESPN API - complete rewrite
from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from datetime import datetime

app = Flask(__name__)

#ESPN Team IDs - COMPLETE LIST
ESPN_TEAMS = {
	"arizona cardinals": "22",
	"atlanta falcons": "1",
	"baltimore ravens": "33",
	"buffalo bills": "2",
	"carolina panthers": "29",
	"chicago bears": "3",
	"cincinnati bengals": "4",
	"cleveland browns": "5",
	"dallas cowboys": "6",
	"denver broncos": "7",
	"detroit lions": "8",
	"green bay packers": "9",
	"houston texans": "34",
	"indianapolis colts": "11",
	"jacksonville jaguars": "30",
	"kansas city chiefs": "16",
	"las vegas raiders": "13",
	"los angeles chargers": "24",
	"los angeles rams": "14",
	"miami dolphins": "15",
	"minnesota vikings": "16",
	"new england patriots": "17",
	"new orleans saints": "18",
	"new york giants": "19",
	"new york jets": "20",
	"philadelphia eagles": "21",
	"pittsburgh steelers": "23",
	"san francisco 49ers": "25",
	"seattle seahawks": "26",
	"tampa bay buccaneers": "27",
	"tennessee titans": "10",
	"washington commanders": "28"
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
	"patrick mahomes": "3139477",
	"tom brady": "1120",
	"aaron rodgers": "8439",
	"josh allen": "3915511",
	"joe burrow": "4241385",
	"justin jefferson": "4360316",
	"travis kelce": "2577411",
	"christian mccaffrey": "3916388",
	"tyreek hill": "3052976",
	"myles garrett": "3915519"
}

@app.route("/")
def index():
	return render_template("index.html", teams=TEAM_DISPLAY_NAMES, popular_players=POPULAR_PLAYERS)

# Team schedule - ALL GAMES
@app.route("/team/<team_key>")
def team_schedule(team_key):
	if team_key in ESPN_TEAMS:
		team_id = ESPN_TEAMS[team_key]
		display_name = TEAM_DISPLAY_NAMES[team_key]

		#get full team schedule from ESPN
		url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule"
		response = requests.get(url)
		data = response.json()
		
		events = data.get("events", [])

		games = []
		for event in events:
			competitions = event.get("competitions", [{}])[0]
			competitors = competitions.get("competitors", [])
			if len(competitors) >= 2:
				home_team = competitors[0].get("team", {}).get("displayName", "")
				away_team = competitors[1].get("team", {}).get("displayName", "")
				home_score = competitors[0].get("score", {}).get("displayValue", "")
				away_score = competitors[1].get("score", {}).get("displayValue", "")

				game = {
					"date": event.get("date", "")[:10],
					"home_team": home_team,
					"away_team": away_team,
					"home_score": home_score,
					"away_score": away_score,
					"status": event.get("status", {}).get("type", {}).get("state", "Scheduled"),
					"venue": competitions.get("venue", {}).get("fullName", ""),
					"time": event.get("date", "")[11:16] if event.get("date") else "TBD"
				}
				games.append(game)

# Split into completed and upcoming games
		completed_games = [g for g in games if g["status"] == "post"]
		upcoming_games = [g for g in games if g["status"] != "post"]

		return render_template("team_schedule.html", completed_games=completed_games[-10:],
						 upcoming_games=upcoming_games, team_name=display_name, 
						 team_key=team_key, total_games=len(games))
	
	return render_template("search.html", error="Team not found")

# TEAM SEARCH
@app.route("/search", methods=["GET", "POST"])
def search_team():
	if request.method == "POST":
		team_name = request.form.get("team_name", "").lower().strip()

		if team_name in ESPN_TEAMS:
			return redirect(url_for("team_schedule", team_key=team_name))
		else:
			return render_template("search.html", error="Team not found. Try full name (e.g., 'dallas cowboys')", teams=TEAM_DISPLAY_NAMES)

	return render_template("search.html", teams=TEAM_DISPLAY_NAMES) 

# PLAYER SEARCH
@app.route("/players", methods=["GET", "POST"])
def search_players():
	if request.method == "POST":
		player_name = request.form.get("player_name", "").strip()

		if player_name:
			#Search player in ESPN API
			url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/players?search={player_name}"
			response = requests.get(url)
			data = response.json()

			players = data.get("athletes", [])

			return render_template("player_results.html", players=players, search_query=player_name,
						  results_count=len(players))
		
	return render_template("player_search.html", popular_players=POPULAR_PLAYERS)

# PLAYER DETAILS
@app.route("/player/<player_id>")
def player_detail(player_id):
	try:
		# Get player profile and stats
		profile_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/players/{player_id}"
		stats_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/players/{player_id}/statistics"

		profile_response = requests.get(profile_url)
		stats_response = requests.get(stats_url)

		profile_data = profile_response.json()
		stats_data = stats_response.json()

		athlete = profile_data.get("athlete", {})

		player = {
			"id": player_id,
			"name": athlete.get("displayName", ""),
			"position": athlete.get("position", {}).get("displayName", ""),
			"team": athlete.get("team", {}).get("displayName", ""),
			"headshot": athlete.get("headshot", {}).get("href", ""),
			"description": athlete.get("description", ""),
			"age": athlete.get("age", ""),
			"height": athlete.get("displayHeight", ""),
			"weight": athlete.get("displayWeight", ""),
			"college": athlete.get("college", {}).get("name", ""),
			"birth_place": athlete.get("birthPlace", {}).get("city", "") + ", " + athlete.get("birthPlace", {}).get("state", ""),
			"jersey": athlete.get("jersey", ""),
			"experience": athlete.get("experience", {}).get("years", ""),
			"stats": stats_data.get("splits", {}).get("categories", [])
		}

		return render_template("player_detail.html", player=player)
	
	except Exception as e:
		return render_template("player_detail.html", player={}, error=str(e))
	
# LATEST SCORES
@app.route("/scores")
def latest_scores():
	# Get latest NFL scores
	url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
	response = requests.get(url)
	data = response.json()

	events = data.get("events", [])

	games = []
	for event in events:
		competitions = event.get("competitions", [{}])[0]
		competitors = competitions.get("competitors", [])

		if len(competitors) >= 2:
			home_team = competitors[0].get("team", {}).get("displayName", "")
			away_team = competitors[1].get("team", {}).get("displayName", "")
			home_score = competitors[0].get("score", {}).get("displayValue", "")
			away_score = competitors[1].get("score", {}).get("displayValue", "")

			game = {
				"date": event.get("date", "")[:10],
				"home_team": home_team,
				"away_team": away_team,
				"home_score": home_score,
				"away_score": away_score,
				"status": event.get("status", {}).get("type", {}).get("state", ""),
				"time": event.get("date", "")[11:16] if event.get("date") else ""
			}
			games.append(game)

	return render_template("scores.html", games=games)

if __name__ == "__main__":
	app.run(debug=True)
