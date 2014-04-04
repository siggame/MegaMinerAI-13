#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import game_history

class AI(BaseAI):
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
    
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
