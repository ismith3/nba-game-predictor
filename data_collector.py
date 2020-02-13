import requests
import json
from nba_api.stats.endpoints import leaguedashteamstats

from team import Team
from game import Game

import sys
import pymongo
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta

currentSeason = 2019

schedule_url = 'http://data.nba.net/prod/v2/{}/schedule.json'.format(currentSeason)


base_stats = leaguedashteamstats.LeagueDashTeamStats().get_dict()['resultSets'][0]['rowSet']
adv_stats = leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced').get_dict()['resultSets'][0]['rowSet']

def fetchData():
  # get team stats -----------------------------
  for i in range(0, len(base_stats)):
    base = base_stats[i]
    adv = adv_stats[i]

    teamId = base[0]
    name = base[1]
    w = base[3]
    l = base[4]
    offrtg = adv[8]
    defrtg = adv[10]
    fgp = base[9]
    fga = base[8]
    tpp = base[12]
    tpa = base[11]
    atr = adv[14]
    rbd = base[18]
    pace = adv[23]
  
    newTeam = Team(teamId, name, w, l, offrtg, defrtg, fgp, fga, tpp, tpa, atr, rbd, pace)
    newTeam.insert()

    sys.stdout.write('Fetching team data: {}\r'.format(i + 1))
    sys.stdout.flush()
  print('Fetching team data: done ({} objects)'.format(len(base_stats)))

  # get schedule ---------------------------------

  data = json.loads(requests.get(schedule_url).text)
  for i in range(0, len(data['league']['standard'])):
    game = data['league']['standard'][i]
    startTime = datetime.strptime(game['startTimeUTC'], '%Y-%m-%dT%H:%M:%S.000Z')
    home = game['hTeam']
    away = game['vTeam']

    homeScore = int(home['score']) if home['score'] != "" else None
    awayScore = int(away['score']) if away['score'] != "" else None

    outcome = None

    if(home['score'] and away['score']):
      if(homeScore > awayScore):
        outcome = 'home'
      elif(homeScore < awayScore):
        outcome = 'away'
      elif(homeScore == awayScore):
        outcome = 'tie'

    newGame = Game(game['gameId'], startTime, home['teamId'], away['teamId'], outcome)
    newGame.insert()

    sys.stdout.write('Fetching game schedule: {}\r'.format(i + 1))
    sys.stdout.flush()

  print('Fetching game schedule: done ({} objects)'.format(len(data['league']['standard'])))
  formatData()


def formatData():
  client = MongoClient('localhost', 27017)
  db = client.nba
  teams = db.teams

  formatted_data = {}

  data = teams.find()
  for doc in data:
    arr = []
    arr.append(doc['offrtg'])
    arr.append(doc['defrtg'])
    arr.append(doc['fgp'])
    arr.append(doc['fga'])
    arr.append(doc['tpp'])
    arr.append(doc['tpa'])
    arr.append(doc['atr'])
    arr.append(doc['rbd'])
    arr.append(doc['pace'])

    formatted_data[doc['name']] = arr

  if(db.data.find()):
    db.data.drop()
  result = db.data.insert_one(formatted_data)
  if(result):
    print('data formatted successfully')

  client.close()

def printUpcoming():
  client = MongoClient('localhost', 27017)
  db = client.nba

  games = db.games.find({
    'startTime': {
      '$gt': datetime.now()
    }
  })

  teamIndex = db.teamIndex.find()[0]

  for i in range(0, 10):

    print(f"{games[i]['startTime']} {teamIndex[games[i]['away']]} @ {teamIndex[games[i]['home']]}")