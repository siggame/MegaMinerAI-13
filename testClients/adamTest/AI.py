#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Pell, May I?"

  @staticmethod
  def password():
    return "He's bigger, faster, and stronger too."

  ##This function is called once, before your first turn
  def init(self):
    self.enemyMinX = 524
    self.enemyMinY = 234
    self.enemyMaxX = 0
    self.enemyMaxY = 0
    self.minX = 300
    self.minY = 300
    self.maxX = 0
    self.maxY = 0
    self.change = -((self.playerID * 2) - 1)
    for droid in self.droids:
      if droid.owner == self.playerID:
        if self.maxX < droid.x:
          self.maxX = droid.x
        if self.maxY < droid.y:
          self.maxY = droid.y
        if self.minX > droid.x:
          self.minX = droid.x
        if self.minY > droid.y:
          self.minY = droid.y
      else:
        if self.enemyMaxX < droid.x:
          self.enemyMaxX = droid.x
        if self.enemyMaxY < droid.y:
          self.enemyMaxY = droid.y
        if self.enemyMinX > droid.x:
          self.enemyMinX = droid.x
        if self.enemyMinY > droid.y:
          self.enemyMinY = droid.y
    self.minY -= 1
    self.maxY += 1
    if self.playerID == 0:
      self.dropX = self.maxX + 1
      self.dropY = self.minY
      self.startX = self.maxX
    else:
      self.dropX = self.minX - 1
      self.dropY = self.minY
      self.startX = self.minX

    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):

    if self.dropY == self.maxY or self.dropY == self.minY:
      self.players[self.playerID].orbitalDrop((self.mapWidth - 1)*self.playerID, self.dropY, 6)
    else:
      self.players[self.playerID].orbitalDrop(self.dropX, self.dropY, 6)
    self.dropY += 1
    if self.dropY > self.maxY:
      self.dropY = self.minY

    while self.players[self.playerID].scrapAmount >= 70:
      xDROPU = random.randint(0, self.mapWidth/2)
      yDROPU = random.randint(0, self.mapHeight/2)
      if self.playerID == 1:
        xDROPU = self.mapWidth - xDROPU - 1
        yDROPU = self.mapHeight - yDROPU - 1
      while not self.players[self.playerID].orbitalDrop(xDROPU, yDROPU, 6):
        xDROPU = random.randint(0, self.mapWidth)
        yDROPU = random.randint(0, self.mapHeight)
        if self.playerID == 1:
          xDROPU = self.mapWidth - xDROPU - 1
          yDROPU = self.mapHeight - yDROPU - 1

    for droid in self.droids:
      if ((droid.owner == self.playerID and droid.hackedTurnsLeft <= 0) or\
          (droid.owner != self.playerID and droid.hackedTurnsLeft > 0))\
           and droid.variant != 7 and droid.variant != 5 and droid.variant != 4:
        movez = droid.maxMovement
        while movez > 0:
          movey = 1
          droid.operate(droid.x + self.change, droid.y)
          droid.operate(droid.x + self.change, droid.y)
          droid.operate(droid.x - self.change, droid.y)
          droid.operate(droid.x - self.change, droid.y)
          #attack around too
          droid.operate(droid.x, droid.y - 1)
          droid.operate(droid.x, droid.y - 1)
          droid.operate(droid.x, droid.y + 1)
          droid.operate(droid.x, droid.y + 1)

          move = True
          for droid2 in self.droids:
            if droid2.id != droid.id:
              if abs(droid2.y - droid.y) + abs(droid2.x - droid.x) == 1:
                if droid2.owner != droid.owner:
                  move = False

          if move:
            if (droid.x <= self.minX and self.playerID == 0) or \
               (droid.x >= self.maxX and self.playerID == 1):
              if not droid.move(droid.x + self.change, droid.y):
                if not droid.move(droid.x, droid.y - 1):
                  droid.move(droid.x, droid.y + 1)
            else:
              target2 = None
              for target in self.droids:
                distance = 99999
                if target.variant == 7 and target.owner != self.playerID:
                  if abs(target.x - droid.x) + abs(target.y - droid.y) < distance:
                    distance = abs(target.x - droid.x) + abs(target.y - droid.y)
                    target2 = target
              target = target2
              if target.x > droid.x:
                droid.move(droid.x + 1, droid.y)
              elif target.x < droid.x:
                droid.move(droid.x - 1, droid.y)
              elif target.y > droid.y:
                droid.move(droid.x, droid.y + 1)
              elif target.y < droid.y:
                droid.move(droid.x, droid.y - 1)

          droid.operate(droid.x + self.change, droid.y)
          droid.operate(droid.x + self.change, droid.y)
          droid.operate(droid.x - self.change, droid.y)
          droid.operate(droid.x - self.change, droid.y)
          #attack around too
          droid.operate(droid.x, droid.y - 1)
          droid.operate(droid.x, droid.y - 1)
          droid.operate(droid.x, droid.y + 1)
          droid.operate(droid.x, droid.y + 1)
          movez -= 1
      elif droid.variant == 4:
        for droid2 in self.droids:
          if droid2.owner != self.playerID:
            if abs(droid2.x - droid.x) + abs(droid2.y - droid.y) < droid.range:
              droid.operate(droid2.x, droid2.y)
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
