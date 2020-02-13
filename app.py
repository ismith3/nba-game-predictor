import sys
import data_collector
import pymongo
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta

def start():
  print('--- Neural Network CLI ---')
  openInterface()
  
def openInterface():
  while(True):
    cmd = input('> ')
    
    if(cmd == 'exit'):
      print('Shutting down with exit code 0')
      sys.exit(0)
    elif(cmd == 'fetch'):
      data_collector.fetchData()
    elif(cmd == 'upcoming'):
      data_collector.printUpcoming()


start()