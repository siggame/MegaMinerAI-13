from base import *
from matchUtils import *
from objects import *
import networking.config.config
from collections import defaultdict
from networking.sexpr.sexpr import *
import os
import itertools
import scribe
import jsonLogger
import random

Scribe = scribe.Scribe

def loadClassDefaults(cfgFile = "config/defaults.cfg"):
  cfg = networking.config.config.readConfig(cfgFile)
  for className in cfg.keys():
    for attr in cfg[className]:
      setattr(eval(className), attr, cfg[className][attr])

class Match(DefaultGameWorld):
  def __init__(self, id, controller):
    self.id = int(id)
    self.controller = controller
    DefaultGameWorld.__init__(self)
    self.scribe = Scribe(self.logPath())
    if( self.logJson ):
      self.jsonLogger = jsonLogger.JsonLogger(self.logPath())
      self.jsonAnimations = []
      self.dictLog = dict(gameName = "Droids", turns = [])
    self.addPlayer(self.scribe, "spectator")

    self.turnNumber = -1
    self.playerID = -1
    self.gameNumber = id

    self.mapWidth = self.mapWidth
    self.mapHeight = self.mapHeight
    self.maxDroids = self.maxDroids
    self.maxWalls = self.maxWalls
    self.scrapRate = self.scrapRate
    self.maxScrap = self.maxScrap
    
    self.hangartiles = []

    self.grid = None

  #this is here to be wrapped
  def __del__(self):
    pass

  def addPlayer(self, connection, type="player"):
    connection.type = type
    if len(self.players) >= 2 and type == "player":
      return "Game is full"
    if type == "player":
      self.players.append(connection)
      try:
        self.addObject(Player, [connection.screenName, self.startTime, 0]) #['id', 'playerName', 'time', 'scrapAmount']
      except TypeError:
        raise TypeError("Someone forgot to add the extra attributes to the Player object initialization")
    elif type == "spectator":
      self.spectators.append(connection)
      #If the game has already started, send them the ident message
      if (self.turn is not None):
        self.sendIdent([connection])
    return True

  def removePlayer(self, connection):
    if connection in self.players:
      if self.turn is not None:
        winner = self.players[1 - self.getPlayerIndex(connection)]
        self.declareWinner(winner, 'Opponent Disconnected')
      self.players.remove(connection)
    else:
      self.spectators.remove(connection)

  def createhangars(self):
    hangarSize = random.range(self.minHangar, self.maxHangar)
    centerX = int(self.mapWidth/4.0)
    centerY = int(self.mapHeight/2.0)

    for y in range(centerY-hangarSize/2, centerY+hangarSize/2):
      #Player 1
      for x in range(centerX-hangarSize/2, centerX+hangarSize/2):
        self.grid[x][y][0].owner = 0
        self.grid[x][y][0].health = self.maxHangarHealth
        self.hangartiles[(x,y)] = self.grid[x][y][0]
      #Player 2
      for x in range(self.width-(centerX-hangarSize/2)+1, centerX+hangarSize/2):
        self.grid[x][y][0].owner = 1
        self.grid[x][y][0].health = self.maxHangarHealth
        self.hangartiles[(x,y)] = self.grid[x][y][0]

    return

  def start(self):
    if len(self.players) < 2:
      return "Game is not full"
    if self.winner is not None or self.turn is not None:
      return "Game has already begun"

    #TODO: START STUFF
    self.turn = self.players[-1]
    self.turnNumber = -1
    #'x', 'y', 'owner', 'turnsUntilAssembled', 'scrapAmount', 'health']
    self.grid = [[[ self.addObject(Tile,[x, y, 2, 0, 0, 0]) ] for y in range(self.mapHeight)] for x in range(self.mapWidth)]

    self.createhangars()

    statList = ["name", "variant", "cost", "maxAttacks", "maxHealth", "maxMovement", "range", "attack", "maxArmor", "scrapWorth"]
    variants = cfgVariants.values()
    variants.sort(key=lambda variant: variant['variant'])
    for t in variants:
      self.addObject(ModelVariant, [t[value] for value in statList])

    self.varaintStrings = {variants.variant:variants.name for variants in self.objects.modelVariants}

    self.nextTurn()
    return True

  def getTile(self, x, y):
    if (0 <= x < self.mapWidth) and (0 <= y < self.mapHeight):
      return self.grid[x][y][0]
    else:
      return None
    
  def nextTurn(self):
    self.turnNumber += 1
    if self.turn == self.players[0]:
      self.turn = self.players[1]
      self.playerID = 1
    elif self.turn == self.players[1]:
      self.turn = self.players[0]
      self.playerID = 0

    else:
      return "Game is over."

    for obj in self.objects.values():
      obj.nextTurn()

    self.checkWinner()
    if self.winner is None:
      self.sendStatus([self.turn] +  self.spectators)
    else:
      self.sendStatus(self.spectators)
    
    if( self.logJson ):
      self.dictLog['turns'].append(
        dict(
          mapWidth = self.mapWidth,
          mapHeight = self.mapHeight,
          turnNumber = self.turnNumber,
          maxDroids = self.maxDroids,
          maxWalls = self.maxWalls,
          playerID = self.playerID,
          gameNumber = self.gameNumber,
          scrapRate = self.scrapRate,
          maxScrap = self.maxScrap,
          Players = [i.toJson() for i in self.objects.values() if i.__class__ is Player],
          Mappables = [i.toJson() for i in self.objects.values() if i.__class__ is Mappable],
          Droids = [i.toJson() for i in self.objects.values() if i.__class__ is Droid],
          Tiles = [i.toJson() for i in self.objects.values() if i.__class__ is Tile],
          ModelVariants = [i.toJson() for i in self.objects.values() if i.__class__ is ModelVariant],
          animations = self.jsonAnimations
        )
      )
      self.jsonAnimations = []

    self.animations = ["animations"]
    return True

  def checkWinner(self):
    #Get the players, is this necessary? If not, just remove these two lines :3
    player1 = self.objects.players[0]
    player2 = self.objects.players[1]
    
    #Determine if hangars are dead
    allDead1 = True #true if player 1's hangar is dead
    allDead2 = True #true if player 2's hangar is dead
    for tile in self.hangartiles: #this line will likely change after Russley finishes his function
      if tile.owner == 0 and tile.health > 0:
        allDead1 = False
      if tile.owner == 1 and tile.health > 0:
        allDead2 = False
    
    #Crown winner
    if allDead1:
      declareWinner(self.players[1], "Player 1\'s hangar has been destroyed")
      return
    elif allDead2:
      declareWinner(self.players[0], "Player 2\'s hangar has been destroyed")
      return
    elif self.turnNumber >= self.turnLimit:
      total1 = 0
      total2 = 0
      for tile in self.hangartiles:
        if tile.owner == 0:
          total1 += tile.health
        elif tile.owner == 1:
          total2 += tile.health

      #Winner has most health
      if total1 > total2:
        declareWinner(self.players[0], "Player 1\'s hangar has more total health.")
      elif total1 < total2:
        declareWinner(self.players[1], "Player 2\'s hangar has more total health.")
      else:
        declareWinner(self.players[0], "Player 1 wins because both are equally matched.")

  return

  def declareWinner(self, winner, reason=''):
    print "Player", self.getPlayerIndex(self.winner), "wins game", self.id
    self.winner = winner

    msg = ["game-winner", self.id, self.winner.user, self.getPlayerIndex(self.winner), reason]
    
    if( self.logJson ):
      self.dictLog["winnerID"] =  self.getPlayerIndex(self.winner)
      self.dictLog["winReason"] = reason
      self.jsonLogger.writeLog( self.dictLog )
    
    self.scribe.writeSExpr(msg)
    self.scribe.finalize()
    self.removePlayer(self.scribe)

    for p in self.players + self.spectators:
      p.writeSExpr(msg)
    
    self.sendStatus([self.turn])
    self.playerID ^= 1
    self.sendStatus([self.players[self.playerID]])
    self.playerID ^= 1
    self.turn = None
    self.objects.clear()

  def logPath(self):
    return "logs/" + str(self.id)

  @derefArgs(Player, None)
  def talk(self, object, message):
    return object.talk(message, )

  @derefArgs(Player, None, None, None)
  def orbitalDrop(self, object, x, y, type):
    return object.orbitalDrop(x, y, type, )

  @derefArgs(Droid, None, None)
  def move(self, object, x, y):
    return object.move(x, y, )

  @derefArgs(Droid, Droid)
  def operate(self, object, target):
    return object.operate(target, )

  @derefArgs(Tile, None)
  def assemble(self, object, type):
    return object.assemble(type, )


  def sendIdent(self, players):
    if len(self.players) < 2:
      return False
    list = []
    for i in itertools.chain(self.players, self.spectators):
      list += [[self.getPlayerIndex(i), i.user, i.screenName, i.type]]
    for i in players:
      i.writeSExpr(['ident', list, self.id, self.getPlayerIndex(i)])

  def getPlayerIndex(self, player):
    try:
      playerIndex = self.players.index(player)
    except ValueError:
      playerIndex = -1
    return playerIndex

  def sendStatus(self, players):
    for i in players:
      i.writeSExpr(self.status())
      i.writeSExpr(self.animations)
    return True


  def status(self):
    msg = ["status"]

    msg.append(["game", self.mapWidth, self.mapHeight, self.turnNumber, self.maxDroids, self.maxWalls, self.playerID, self.gameNumber, self.scrapRate, self.maxScrap])

    typeLists = []
    typeLists.append(["Player"] + [i.toList() for i in self.objects.values() if i.__class__ is Player])
    typeLists.append(["Mappable"] + [i.toList() for i in self.objects.values() if i.__class__ is Mappable])
    typeLists.append(["Droid"] + [i.toList() for i in self.objects.values() if i.__class__ is Droid])
    updated = [i for i in self.objects.values() if i.__class__ is Tile and i.updatedAt > self.turnNumber-3]
    if updated:
      typeLists.append(["Tile"] + [i.toList() for i in updated])
    updated = [i for i in self.objects.values() if i.__class__ is ModelVariant and i.updatedAt > self.turnNumber-3]
    if updated:
      typeLists.append(["ModelVariant"] + [i.toList() for i in updated])

    msg.extend(typeLists)

    return msg

  def addAnimation(self, anim):
    # generate the sexp
    self.animations.append(anim.toList())
    # generate the json
    if( self.logJson ):
      self.jsonAnimations.append(anim.toJson())
  


loadClassDefaults()

