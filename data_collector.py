import requests
import json
from nba_api.stats.endpoints import leaguedashteamstats

currentSeason = 2019

schedule_url = 'http://data.nba.net/prod/v2/{}/schedule.json'.format(currentSeason)


base_stats = leaguedashteamstats.LeagueDashTeamStats().get_dict()
adv_stats = leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced').get_json()

for team in base_stats['resultSets'][0]['rowSet']:
  name = team[1]
  w = team[3]
  l = team[4]
  
  print(name, w, l)