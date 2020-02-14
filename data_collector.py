import requests
import json
from nba_api.stats.endpoints import leaguedashteamstats

from team import Team
from game import Game

import sys
import pymongo
from pymongo import MongoClient
from datetime import datetime, date
import dateutil.parser
from dateutil.tz import tzlocal
import pytz
from pytz import timezone

currentSeason = 2019

schedule_url = 'http://data.nba.net/prod/v2/{}/schedule.json'.format(currentSeason)


base_stats = leaguedashteamstats.LeagueDashTeamStats().get_dict()['resultSets'][0]['rowSet']
adv_stats = leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced').get_dict()['resultSets'][0]['rowSet']

fmt = "%Y-%m-%d %H:%M:%S %Z%z"

client = MongoClient('localhost', 27017)
db = client.nba

teamIndex = db.teamIndex.find({})[0]

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
  count = 0

  for game in data['league']['standard']:
    # startTimeUTC = startTime.replace(tzinfo=timezone('UTC'))
    #startTimeCentral = startTime.astimezone(tzlocal())
    #print(startTimeCentral)
    

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

    if(teamIndex.get(home['teamId'], False) and teamIndex.get(away['teamId'], False)):
      newGame = Game(game['gameId'], game['startTimeUTC'], home['teamId'], away['teamId'], outcome)
      newGame.insert()
      count += 1

    sys.stdout.write('Fetching game schedule: {}\r'.format(count + 1))
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
    print('Data formatted successfully')

def printUpcoming():
  games = db.games.find({
    
  })

  for game in games:
    utc = pytz.UTC
    #
    startTime = dateutil.parser.parse(game['startTime'])
    if(startTime.replace(tzinfo=utc) > datetime.now().replace(tzinfo=utc)):
      print(startTime.astimezone(tzlocal()))#.strftime(fmt))#.astimezone(tzlocal()), teamIndex[games[i]['away']], teamIndex[games[i]['home']])

  # for i in range(0, 10):
  #   localTimeString = games[i]['startTime'].astimezone(timezone('US/Central'))
  #   print(games[i]['away'])
  #   print(f"{localTimeString.strftime(fmt)} {teamIndex[games[i]['away']]} @ {teamIndex[games[i]['home']]}")