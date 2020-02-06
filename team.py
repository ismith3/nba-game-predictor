class Team:
  def __init__(self, name, w, l, offrtg, defrtg, fgp, fga, tpp, tpa, atr, rbd, pace):
    self.name = name
    self.w = w
    self.l = l
    self.offrtg = offrtg
    self.defrtg = defrtg
    self.fgp = fgp
    self.fga = fga
    self.tpp = tpp
    self.tpa = tpa
    self.atr = atr
    self.rbd = rbd
    self.pace = pace
  
  def insert(self):
    import pymongo
    from pymongo import MongoClient

    client = MongoClient('localhost', 27017)
    db = client.nba

    teams = db.teams

    if(teams.find_one({'name': self.name})) != None:
      print('already exists in db')
    else:
      post_id = teams.insert_one(self).inserted_id
      print(post_id)
