#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "The BIRDS of Skyrim"

  @staticmethod
  def password():
    return "53282f00d1a0a60"

  ##This function is called once, before your first turn
  def init(self):
    self.hasSpawned = False
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
    if not self.hasSpawned and random.randint(0, 99) <= 10:
      self.hasSpawned = True
    meh = self.randVars[random.randint(0,len(self.randVars) - 1)]
    if self.players[self.playerID].scrapAmount >= 90:
      if self.hasSpawned:
        bleh = 0
        while bleh < 10:
          bleh += 1
          xDROPU = random.randint(0, 1)
          yDROPU = random.randint(0, self.mapHeight - 1)
          if self.playerID == 1:
            xDROPU = self.mapWidth - xDROPU - 1
            yDROPU = self.mapHeight - yDROPU - 1
          if self.players[self.playerID].scrapAmount > self.modelVariants[meh].cost:
            if self.meh(xDROPU, yDROPU) is None:
              self.players[self.playerID].orbitalDrop(xDROPU, yDROPU, meh)
            else:
              self.hasSpawned = True
              bleh = 20
          else:
            bleh = 30
      else:
        self.hasSpawned = False
        for base in self.droids:
          if base.variant == 7 and base.owner != self.playerID:
            if self.meh(base.x + 1, base.y) is None:
              self.players[self.playerID].orbitalDrop(base.x + 1, base.y, 4)
              break
            if self.meh(base.x - 1, base.y) is None:
              self.players[self.playerID].orbitalDrop(base.x - 1, base.y, 4)
              break
            if self.meh(base.x, base.y + 1) is None:
              self.players[self.playerID].orbitalDrop(base.x, base.y + 1, 4)
              break
            if self.meh(base.x, base.y - 1) is None:
              self.players[self.playerID].orbitalDrop(base.x, base.y - 1, 4)
              break

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
            if droid2.owner == self.playerID and droid2.id != droid.id and (droid2.maxArmor != droid2.armor or droid2.hackets > 0):
              if abs(droid2.x - droid.x) + abs(droid2.y - droid.y) <= droid.range + droid.maxMovement:
                bleh.append(droid2)
          if len(bleh) == 0:
            bleh.append(droid)
        #attack even if a turret
        for droid2 in bleh:
          for _ in range(droid.maxAttacks):
            if self.okay(droid, droid2):
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
            if target.owner == self.playerID and target.id != droid.id:
              if (abs(target.x - droid.x) + abs(target.y - droid.y)) < self.distance:
                self.distance = (abs(target.x - droid.x) + abs(target.y - droid.y))
                target2 = target
          else:
            if target.owner != self.playerID and target.hackedTurnsLeft == 0:
              if target.variant != 5 and target.variant != 7 and target.attack > 0:
                if (abs(target.x - droid.x) + abs(target.y - droid.y)) < self.distance:
                  self.distance = (abs(target.x - droid.x) + abs(target.y - droid.y))
                  target2 = target

        target = target2

        movez = droid.maxMovement

        while movez > 0:
          movez -= 1
          movey = 1

          for droid2 in bleh:
            for _ in range(droid.maxAttacks):
              if self.okay(droid, droid2):
                droid.operate(droid2.x, droid2.y)

          move = True
          for droid2 in self.droids:
            if droid2.id != droid.id:
              if abs(droid2.y - droid.y) + abs(droid2.x - droid.x) <= droid.range:
                if droid2.owner != (self.playerID ^ (droid2.hackedTurnsLeft > 0)) and droid.attack > 0:
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

  def dist(self, me, you):
    return abs(me.x  - you.x) + abs(me.y - you.y)

  def okay(self, me, target):
    if me.attacksLeft == 0 or target.healthLeft == 0:
      return False
    if me.variant == 3:
      if target.owner != self.playerID and target.hackedTurnsLeft == 0 and self.dist(me, target) <= me.range:
        return True
    elif me.attack < 0:
      if target.owner == self.playerID and self.dist(me, target) <= me.range and (target.maxArmor != target.armor or target.hackets > 0):
        return True
    else:
      if target.owner != (self.playerID ^ (target.hackedTurnsLeft > 0)) and self.dist(me, target) <= me.range:
        return True
    return False

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
