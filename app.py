# Nfl App with ESPN API - complete rewrite
from flask import Flask, render_template, request
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
	"cincinatti bengals": "4",
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
	"cincinatti bengals": "Cincinatti Bengals",
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
