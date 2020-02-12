class Team():
  def __init__(self, teamId, name, w, l, offrtg, defrtg, fgp, fga, tpp, tpa, atr, rbd, pace):
    self.data = {
      'teamId': teamId,
      'name': name,
      'w': w,
      'l': l,
      'offrtg': offrtg,
      'defrtg': defrtg,
      'fgp': fgp,
      'fga': fga,
      'tpp': tpp,
      'tpa': tpa,
      'atr': atr,
      'rbd': rbd,
      'pace': pace
    }
  
  def insert(self):
    import json
    import pymongo
    from pymongo import MongoClient

    client = MongoClient('localhost', 27017)
    db = client.nba

    teams = db.teams

    if(teams.find_one({'name': self.data['name']})) != None:
      result = teams.update_one({'name': self.data['name']}, {'$set': self.data})
      return result.acknowledged
    else:
      post_id = teams.insert_one(self.data).inserted_id
      if(post_id): return True
      return False
