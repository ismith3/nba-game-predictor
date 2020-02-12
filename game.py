import pymongo
from pymongo import MongoClient

class Game():
  def __init__(self, gameId, startTime, home, away, outcome):
    self.data = {
      'gameId': gameId,
      'startTime': startTime,
      'home': home,
      'away': away,
      'outcome': outcome
    }

  def insert(self):
    client = MongoClient('localHost', 27017)
    games = client.nba.games

    if(games.find_one({'gameId': self.data['gameId']})) != None:
      result = games.update_one({'gameId': self.data['gameId']}, {'$set': self.data})
      return result.acknowledged
    else:
      post_id = games.insert_one(self.data).inserted_id
      if(post_id): return True
      return False
