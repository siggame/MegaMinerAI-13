# -*- python -*-

from library import library

class BaseAI:
  """@brief A basic AI interface.

  This class implements most the code an AI would need to interface with the lower-level game code.
  AIs should extend this class to get a lot of builer-plate code out of the way
  The provided AI class does just that.
  """
  #\cond
  initialized = False
  iteration = 0
  runGenerator = None
  connection = None
  #\endcond
  players = []
  mappables = []
  droids = []
  tiles = []
  modelVariants = []
  #\cond
  def startTurn(self):
    from GameObject import Player
    from GameObject import Mappable
    from GameObject import Droid
    from GameObject import Tile
    from GameObject import ModelVariant

    BaseAI.players = [Player(library.getPlayer(self.connection, i)) for i in xrange(library.getPlayerCount(self.connection))]
    BaseAI.mappables = [Mappable(library.getMappable(self.connection, i)) for i in xrange(library.getMappableCount(self.connection))]
    BaseAI.droids = [Droid(library.getDroid(self.connection, i)) for i in xrange(library.getDroidCount(self.connection))]
    BaseAI.tiles = [Tile(library.getTile(self.connection, i)) for i in xrange(library.getTileCount(self.connection))]
    BaseAI.modelVariants = [ModelVariant(library.getModelVariant(self.connection, i)) for i in xrange(library.getModelVariantCount(self.connection))]

    if not self.initialized:
      self.initialized = True
      self.init()
    BaseAI.iteration += 1;
    if self.runGenerator:
      try:
        return self.runGenerator.next()
      except StopIteration:
        self.runGenerator = None
    r = self.run()
    if hasattr(r, '__iter__'):
      self.runGenerator = r
      return r.next()
    return r
  #\endcond
  #\cond
  def getMapWidth(self):
    return library.getMapWidth(self.connection)
  #\endcond
  mapWidth = property(getMapWidth)
  #\cond
  def getMapHeight(self):
    return library.getMapHeight(self.connection)
  #\endcond
  mapHeight = property(getMapHeight)
  #\cond
  def getTurnNumber(self):
    return library.getTurnNumber(self.connection)
  #\endcond
  turnNumber = property(getTurnNumber)
  #\cond
  def getMaxDroids(self):
    return library.getMaxDroids(self.connection)
  #\endcond
  maxDroids = property(getMaxDroids)
  #\cond
  def getPlayerID(self):
    return library.getPlayerID(self.connection)
  #\endcond
  playerID = property(getPlayerID)
  #\cond
  def getGameNumber(self):
    return library.getGameNumber(self.connection)
  #\endcond
  gameNumber = property(getGameNumber)
  #\cond
  def getScrapRate(self):
    return library.getScrapRate(self.connection)
  #\endcond
  scrapRate = property(getScrapRate)
  #\cond
  def getMaxScrap(self):
    return library.getMaxScrap(self.connection)
  #\endcond
  maxScrap = property(getMaxScrap)
  #\cond
  def getDropTime(self):
    return library.getDropTime(self.connection)
  #\endcond
  dropTime = property(getDropTime)
  def __init__(self, connection):
    self.connection = connection
