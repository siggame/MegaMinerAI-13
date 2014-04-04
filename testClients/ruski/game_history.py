import copy
import time
import sys

def get_tile(ai, x, y):
  if (0 <= x < ai.mapWidth) and (0 <= y < ai.mapHeight):
    return ai.tiles[x * ai.mapHeight + y]
  else:
    return None

class game_history:
  def __init__(self, ai, use_colors = False):
    self.use_colors = use_colors
    self.history = []
    self.ai = ai

    self.BLACK = 0
    self.RED = 1
    self.GREEN = 2
    self.YELLOW = 3
    self.BLUE = 4
    self.MAGENTA = 5
    self.CYAN = 6
    self.WHITE = 7

    #SET UP THE PARTS THAT ARE NOT MOVING
  def colorText(self, text, fgcolor = None, bgcolor = None):
    if self.use_colors and fgcolor and bgcolor:
      return '\x1b[3{};4{};1m'.format(fgcolor, bgcolor) + text + '\x1b[0m'
    elif self.use_colors and fgcolor:
      return '\x1b[3{};1m'.format(fgcolor) + text + '\x1b[0m'
    else:
      return text

  def save_snapshot(self):
    tempGrid = [[[] for _ in range( self.ai.mapHeight ) ] for _ in range( self.ai.mapWidth ) ]

    for tile in self.ai.tiles:
      if tile.turnsUntilAssembled > 0:
        tempGrid[tile.x][tile.y].append(self.colorText('S', self.WHITE, self.GREEN))

    for droid in self.ai.droids:
      if droid.owner == self.ai.playerID:
          tempGrid[droid.x][droid.y].append(self.colorText(str(droid.variant), self.RED, self.BLACK))
      elif droid.owner == self.ai.playerID^1:
          tempGrid[droid.x][droid.y].append(self.colorText(str(droid.variant), self.BLUE, self.BLACK))

    #self.print_snapshot(tempGrid)
    self.history.append(tempGrid)
    return tempGrid

  def print_snapshot(self, snapshot):
    print('--' * self.ai.mapWidth)
    for y in range(self.ai.mapHeight):
      for x in range(self.ai.mapWidth):
        if len(snapshot[x][y]) > 0:
          print(snapshot[x][y][0]),
        else:
          print(' '),
      print
    return

  def print_history(self):
    turnNumber = 0
    for snapshot in self.history:
      print(turnNumber)
      turnNumber += 1
      self.print_snapshot(snapshot)
      time.sleep(.1)

