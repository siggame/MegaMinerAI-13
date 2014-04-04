#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import random

import game_history
import game_cache

class AI(BaseAI):

  self.manhattan_offsets = [(0,1),(0,-1),(1,0),(-1,0)]

  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  ##This function is called once, before your first turn
  def init(self):
    self.history = game_history.game_history(self, True)
    self.cache = game_cache.game_cache(self)
    pass

  ##This function is called once, after your last turn
  def end(self):
    self.history.print_history()
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    snapshot = self.history.save_snapshot()
    self.history.print_snapshot(snapshot)
    self.game_cache.update_all()

    #DROP SOMETHING
    randx = random.randrange(0, self.mapWidth-1)
    randy = random.randrange(0, self.mapHeight-1)
    randv = random.randrange(0, 7)
    self.players[self.playerID].orbitalDrop(randx, randy, randv)

    for droid in self.droids:
      if droid.owner == self.playerID:
        offset = random.choice(self.manhattan_offsets)
        droid.move(offset[0], offset[1])

        offset = random.choice(self.manhattan_offsets)
        droid.operate(offset[0], offset[1])

    
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
