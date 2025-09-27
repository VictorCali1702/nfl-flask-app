# NFL APP in FLASK
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
	return "Hello NFL!"

if __name__ == "__main__":
	app.run(debug=True)
	