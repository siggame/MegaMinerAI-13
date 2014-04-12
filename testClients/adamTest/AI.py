#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return unicode("Pell, May I?")

  @staticmethod
  def password():
    return "He's bigger, faster, and stronger too."

  ##This function is called once, before your first turn
  def init(self):
    self.change = -((self.playerID * 2) - 1)
    pass

  ##This function is called once, after your last turn
  def end(self):
    print "This was called"
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information

  randVars = [0,1,2,3,6]

  def run(self):
    meh = self.randVars[random.randint(0,len(self.randVars) - 1)]
    if self.players[self.playerID].scrapAmount > 80:
      bleh = 0
      while bleh < 10:
        bleh += 1
        xDROPU = random.randint(0, 1)
        yDROPU = random.randint(0, self.mapHeight/2)
        if self.playerID == 1:
          xDROPU = self.mapWidth - xDROPU - 1
          yDROPU = self.mapHeight - yDROPU - 1
        if self.players[self.playerID].scrapAmount > self.modelVariants[meh].cost:
          self.players[self.playerID].orbitalDrop(xDROPU, yDROPU, meh)

    for droid in self.droids:
      if droid.healthLeft == 0:
        continue
      if ((droid.owner == self.playerID and droid.hackedTurnsLeft <= 0) or\
          (droid.owner != self.playerID and droid.hackedTurnsLeft > 0))\
           and droid.variant != 7 and droid.variant != 5:
        bleh = []
        if droid.variant == 3:
          for droid2 in self.droids:
            if droid2.owner != self.playerID and droid2.variant != 7 and droid2.variant != 5:
              if abs(droid2.x - droid.x) + abs(droid2.y - droid.y) <= droid.range + droid.maxMovement:
                bleh.append(droid2)
        elif droid.attack > 0:
          for droid2 in self.droids:
            if droid2.owner != (self.playerID ^ (droid2.hackedTurnsLeft > 0)):
              if abs(droid2.x - droid.x) + abs(droid2.y - droid.y) <= droid.range + droid.maxMovement:
                bleh.append(droid2)
        else:
          for droid2 in self.droids:
            if droid2.owner == self.playerID and droid2.maxArmor != droid2.armor:
              if abs(droid2.x - droid.x) + abs(droid2.y - droid.y) <= droid.range + droid.maxMovement:
                bleh.append(droid2)
        #attack even if a turret
        for droid2 in bleh:
          if abs(droid2.x - droid.x) + abs(droid2.y - droid.y) <= droid.range and droid.attacksLeft > 0:
            droid.operate(droid2.x, droid2.y)

        target2 = None
        self.distance = 99999
        for target in self.droids:
          if droid.attack > 0 and droid.variant != 3:
            if target.variant == 7 and target.owner != self.playerID:
              if (abs(target.x - droid.x) + abs(target.y - droid.y)) < self.distance:
                self.distance = (abs(target.x - droid.x) + abs(target.y - droid.y))
                target2 = target
          elif droid.attack < 0:
            if target.variant != 7 and target.owner == self.playerID and target.id != droid.id and droid2.maxArmor != droid2.armor:
              if (abs(target.x - droid.x) + abs(target.y - droid.y)) < self.distance:
                self.distance = (abs(target.x - droid.x) + abs(target.y - droid.y))
                target2 = target
          else:
            if target.owner != self.playerID and target.hackedTurnsLeft == 0:
              if target.variant != 7 and target.variant != 5:
                if (abs(target.x - droid.x) + abs(target.y - droid.y)) < self.distance:
                  self.distance = (abs(target.x - droid.x) + abs(target.y - droid.y))
                  target2 = target

        target = target2

        movez = droid.maxMovement

        while movez > 0:
          movez -= 1
          movey = 1

          for droid2 in bleh:
            if abs(droid2.x - droid.x) + abs(droid2.y - droid.y) <= droid.range and droid.attacksLeft > 0:
              droid.operate(droid2.x, droid2.y)

          move = True
          for droid2 in self.droids:
            if droid2.id != droid.id:
              if abs(droid2.y - droid.y) + abs(droid2.x - droid.x) <= droid.range:
                if droid2.owner != (self.playerID ^ (droid2.hackedTurnsLeft > 0)):
                  move = False

          if move and droid.movementLeft > 0:
            if target is not None:
              if target.x > droid.x:
                if self.meh(droid.x + 1, droid.y) is None and droid.x != self.mapWidth - 1:
                  droid.move(droid.x + 1, droid.y)
                elif self.meh(droid.x, droid.y - 1) is None and droid.y != 0:
                  droid.move(droid.x, droid.y - 1)
                elif self.meh(droid.x, droid.y + 1) is None and droid.y != self.mapHeight - 1:
                  droid.move(droid.x, droid.y + 1)
              elif target.x < droid.x:
                if self.meh(droid.x - 1, droid.y) is None and droid.x != 0:
                  droid.move(droid.x - 1, droid.y)
                elif self.meh(droid.x, droid.y - 1) is None and droid.y != 0:
                  droid.move(droid.x, droid.y - 1)
                elif self.meh(droid.x, droid.y + 1) is None and droid.y != self.mapHeight - 1:
                  droid.move(droid.x, droid.y + 1)
              elif target.y > droid.y:
                if self.meh(droid.x, droid.y + 1) is None and droid.y != self.mapHeight - 1:
                  droid.move(droid.x, droid.y + 1)
                elif self.meh(droid.x - 1, droid.y) is None and droid.x != 0:
                  droid.move(droid.x - 1, droid.y)
                elif self.meh(droid.x + 1, droid.y) is None and droid.x != self.mapWidth - 1:
                  droid.move(droid.x + 1, droid.y )
              elif target.y < droid.y:
                if self.meh(droid.x, droid.y - 1) is None and droid.y != 0:
                  droid.move(droid.x, droid.y - 1)
                elif self.meh(droid.x - 1, droid.y) is None and droid.x != 0:
                  droid.move(droid.x - 1, droid.y)
                elif self.meh(droid.x + 1, droid.y) is None and droid.x != self.mapWidth - 1:
                  droid.move(droid.x + 1, droid.y )
    return 1

  def meh(self, x, y):
    for droid in self.droids:
      if x == droid.x and y == droid.y:
        return droid
    return None

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
