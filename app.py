# NFL APP in FLASK
from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/games")
def games():
	url = "https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id=134922"
	response = requests.get(url)
	data = response.json()

	games = data.get("results", []) # list of matches
	return render_template("games.html", games=games)


if __name__ == "__main__":
	app.run(debug=True)
