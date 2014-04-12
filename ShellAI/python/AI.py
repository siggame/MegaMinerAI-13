#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  CLAW, ARCHER, REPAIRER, HACKER, TURRET, WALL, TERMINATOR, HANGAR = range(8)

  ##This function is called once, before your first turn
  def init(self):
    offset = 0
    found = False
    #find a location without a hangar
    while not found:
      for tile in self.tiles:
        #make sure tile is near the edge
        if tile.x == (self.mapWidth - 1) * self.playerID + offset:
          hangarPresent = False
          #check for hangar
          for droid in self.droids:
            if droid.x == tile.x and droid.y == tile.y:
              hangarPresent = True
              break
          if not hangarPresent:
            self.spawnX = tile.x
            self.spawnY = tile.y
            found = True
            break
      #if nothing was found move away from the edge
      if not found:
        if self.playerID == 0:
          offset += 1
        else:
          offset -= 1
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    #try to spawn a claw near your side
    #make sure you own enough scrap
    if self.players[self.playerID].scrapAmount >= self.modelVariants[self.CLAW].cost:
      #make sure nothing is spawning there
      if self.getTile(self.spawnX, self.spawnY).turnsUntilAssembled == 0:
        spawn = True
        #make sure there isn't a hangar
        for droid in self.droids:
          #if the droid's x and y is the same as the spawn point
          if droid.x == self.spawnX and droid.y == self.spawnY:
            #if the droid is a hangar
            if droid.variant == self.HANGAR:
              #can't spawn on top of hangars
              spawn = False
              break
        if spawn:
          #spawn the claw
          self.players[self.playerID].orbitalDrop(self.spawnX, self.spawnY, self.CLAW)
      #loop through all of the droids
      for droid in self.droids:
        #if you have control of the droid
        if (droid.owner == self.playerID and droid.hackedTurnsLeft <= 0) or (droid.owner != self.playerID and droid.hackedTurnsLeft > 0):
          #if there are any moves to be done
          if droid.movementLeft > 0:
            #try to move towards the enemy
            changeX = 1
            #if on the right move towards the left
            if self.playerID == 1:
              changeX = -1
            move = True
            #check if there is a droid on that tile
            for droid2 in self.droids:
              #if the droids are different
              if droid.id != droid2.id:
                #if there is a droid to run into
                if droid2.x == droid.x + changeX and droid2.y == droid.y:
                  #don't move
                  move = False
            #move if okay and within map boundaries
            if move and (droid.x + changeX >= 0) and (droid.x + changeX < self.mapWidth):
              droid.move(droid.x + changeX, droid.y)
            #if there are any attacks left
            if droid.attacksLeft > 0:
              #find a target towards the enemy
              changeX = 1
              #enemy is to the left if playerID is one
              if self.playerID == 1:
                changeX = -1
              target = None
              for droid2 in self.droids:
                #if the droid there make it a target
                if droid2.x == droid.x + changeX and droid2.y == droid.y:
                  target = droid2
              #if a target was found
              if target is not None:
                #repaier logic
                if droid.variant == self.REPAIRER:
                  #only try to heal your units or hacked enemy units
                  if (target.owner == self.playerID and target.hackedTurnsLeft <= 0) or (target.owner != self.playerID and target.hackedTurnsLeft > 0):
                    #heal the target
                    droid.operate(target.x, target.y)
                #hacker unit logic
                elif droid.variant == self.HACKER:
                  #only operate on non-hacked enemy units
                  if target.owner != self.playerID and target.hackedTurnsLeft == 0:
                    #don't hack hangars or walls
                    if target.variant != self.HANGAR and target.variant != self.WALL:
                      #hack the target
                      droid.operate(target.x, target.y)
                #other unit logic
                else:
                  #only operate on hacked friendly units or enemy units
                  if (target.owner == self.playerID and target.hackedTurnsLeft > 0) or (target.owner != self.playerID and target.hackedTurnsLeft <= 0):
                    #attack the target
                    droid.operate(target.x, target.y)
    return 1

  #returns a tile, or None if no tile
  def getTile(self, x ,y):
    for tile in self.tiles:
      if tile.x == x and tile.y == y:
        return tile
    return None

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
