# -*- python -*-

from library import library

from ExistentialError import ExistentialError

class GameObject(object):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration


##
class Player(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.playerGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.players:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  ##Allows a player to display messages on the screen
  def talk(self, message):
    self.validify()
    return library.playerTalk(self._ptr, message)

  ##Allows a player to spawn a Droid.
  def orbitalDrop(self, x, y, variant):
    self.validify()
    return library.playerOrbitalDrop(self._ptr, x, y, variant)

  #\cond
  def getId(self):
    self.validify()
    return library.playerGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getPlayerName(self):
    self.validify()
    return library.playerGetPlayerName(self._ptr)
  #\endcond
  ##Player's Name
  playerName = property(getPlayerName)

  #\cond
  def getTime(self):
    self.validify()
    return library.playerGetTime(self._ptr)
  #\endcond
  ##Time remaining, updated at start of turn
  time = property(getTime)

  #\cond
  def getScrapAmount(self):
    self.validify()
    return library.playerGetScrapAmount(self._ptr)
  #\endcond
  ##The amount of scrap you have in your Hangar.
  scrapAmount = property(getScrapAmount)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "playerName: %s\n" % self.getPlayerName()
    ret += "time: %s\n" % self.getTime()
    ret += "scrapAmount: %s\n" % self.getScrapAmount()
    return ret

##A mappable object!
class Mappable(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.mappableGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.mappables:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  #\cond
  def getId(self):
    self.validify()
    return library.mappableGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getX(self):
    self.validify()
    return library.mappableGetX(self._ptr)
  #\endcond
  ##X position of the object
  x = property(getX)

  #\cond
  def getY(self):
    self.validify()
    return library.mappableGetY(self._ptr)
  #\endcond
  ##Y position of the object
  y = property(getY)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    return ret

##Represents a single Droid on the map.
class Droid(Mappable):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.droidGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.droids:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  ##Make the Droid move to the respective x and y location.
  def move(self, x, y):
    self.validify()
    return library.droidMove(self._ptr, x, y)

  ##Command to operate (repair, attack, hack) on another Droid.
  def operate(self, x, y):
    self.validify()
    return library.droidOperate(self._ptr, x, y)

  #\cond
  def getId(self):
    self.validify()
    return library.droidGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getX(self):
    self.validify()
    return library.droidGetX(self._ptr)
  #\endcond
  ##X position of the object
  x = property(getX)

  #\cond
  def getY(self):
    self.validify()
    return library.droidGetY(self._ptr)
  #\endcond
  ##Y position of the object
  y = property(getY)

  #\cond
  def getOwner(self):
    self.validify()
    return library.droidGetOwner(self._ptr)
  #\endcond
  ##The owner of this Droid.
  owner = property(getOwner)

  #\cond
  def getVariant(self):
    self.validify()
    return library.droidGetVariant(self._ptr)
  #\endcond
  ##The variant of this Droid. This variant refers to list of ModelVariants.
  variant = property(getVariant)

  #\cond
  def getAttacksLeft(self):
    self.validify()
    return library.droidGetAttacksLeft(self._ptr)
  #\endcond
  ##The number of attacks the Droid has remaining.
  attacksLeft = property(getAttacksLeft)

  #\cond
  def getMaxAttacks(self):
    self.validify()
    return library.droidGetMaxAttacks(self._ptr)
  #\endcond
  ##The maximum number of times the Droid can attack.
  maxAttacks = property(getMaxAttacks)

  #\cond
  def getHealthLeft(self):
    self.validify()
    return library.droidGetHealthLeft(self._ptr)
  #\endcond
  ##The current amount health this Droid has remaining.
  healthLeft = property(getHealthLeft)

  #\cond
  def getMaxHealth(self):
    self.validify()
    return library.droidGetMaxHealth(self._ptr)
  #\endcond
  ##The maximum amount of this health this Droid can have
  maxHealth = property(getMaxHealth)

  #\cond
  def getMovementLeft(self):
    self.validify()
    return library.droidGetMovementLeft(self._ptr)
  #\endcond
  ##The number of moves this Droid has remaining.
  movementLeft = property(getMovementLeft)

  #\cond
  def getMaxMovement(self):
    self.validify()
    return library.droidGetMaxMovement(self._ptr)
  #\endcond
  ##The maximum number of moves this Droid can move.
  maxMovement = property(getMaxMovement)

  #\cond
  def getRange(self):
    self.validify()
    return library.droidGetRange(self._ptr)
  #\endcond
  ##The range of this Droid's attack.
  range = property(getRange)

  #\cond
  def getAttack(self):
    self.validify()
    return library.droidGetAttack(self._ptr)
  #\endcond
  ##The power of this Droid variant's attack.
  attack = property(getAttack)

  #\cond
  def getArmor(self):
    self.validify()
    return library.droidGetArmor(self._ptr)
  #\endcond
  ##How much armor the Droid has which reduces damage taken.
  armor = property(getArmor)

  #\cond
  def getMaxArmor(self):
    self.validify()
    return library.droidGetMaxArmor(self._ptr)
  #\endcond
  ##How much armor the Droid has which reduces damage taken.
  maxArmor = property(getMaxArmor)

  #\cond
  def getScrapWorth(self):
    self.validify()
    return library.droidGetScrapWorth(self._ptr)
  #\endcond
  ##The amount of scrap the Droid drops.
  scrapWorth = property(getScrapWorth)

  #\cond
  def getTurnsToBeHacked(self):
    self.validify()
    return library.droidGetTurnsToBeHacked(self._ptr)
  #\endcond
  ##The number of turns this unit will be hacked, if it is hacked. If 0, the droid cannot be hacked.
  turnsToBeHacked = property(getTurnsToBeHacked)

  #\cond
  def getHackedTurnsLeft(self):
    self.validify()
    return library.droidGetHackedTurnsLeft(self._ptr)
  #\endcond
  ##The number of turns the Droid has remaining as hacked.
  hackedTurnsLeft = property(getHackedTurnsLeft)

  #\cond
  def getHackets(self):
    self.validify()
    return library.droidGetHackets(self._ptr)
  #\endcond
  ##The amount of hacking progress that has been made.
  hackets = property(getHackets)

  #\cond
  def getHacketsMax(self):
    self.validify()
    return library.droidGetHacketsMax(self._ptr)
  #\endcond
  ##The maximum number of hackets that can be sustained before hacked. If 0, the Droid cannot be hacked.
  hacketsMax = property(getHacketsMax)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "owner: %s\n" % self.getOwner()
    ret += "variant: %s\n" % self.getVariant()
    ret += "attacksLeft: %s\n" % self.getAttacksLeft()
    ret += "maxAttacks: %s\n" % self.getMaxAttacks()
    ret += "healthLeft: %s\n" % self.getHealthLeft()
    ret += "maxHealth: %s\n" % self.getMaxHealth()
    ret += "movementLeft: %s\n" % self.getMovementLeft()
    ret += "maxMovement: %s\n" % self.getMaxMovement()
    ret += "range: %s\n" % self.getRange()
    ret += "attack: %s\n" % self.getAttack()
    ret += "armor: %s\n" % self.getArmor()
    ret += "maxArmor: %s\n" % self.getMaxArmor()
    ret += "scrapWorth: %s\n" % self.getScrapWorth()
    ret += "turnsToBeHacked: %s\n" % self.getTurnsToBeHacked()
    ret += "hackedTurnsLeft: %s\n" % self.getHackedTurnsLeft()
    ret += "hackets: %s\n" % self.getHackets()
    ret += "hacketsMax: %s\n" % self.getHacketsMax()
    return ret

##Represents a single tile on the map.
class Tile(Mappable):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.tileGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.tiles:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  #\cond
  def getId(self):
    self.validify()
    return library.tileGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getX(self):
    self.validify()
    return library.tileGetX(self._ptr)
  #\endcond
  ##X position of the object
  x = property(getX)

  #\cond
  def getY(self):
    self.validify()
    return library.tileGetY(self._ptr)
  #\endcond
  ##Y position of the object
  y = property(getY)

  #\cond
  def getOwner(self):
    self.validify()
    return library.tileGetOwner(self._ptr)
  #\endcond
  ##Owner of spawning droid. 0 - Player 1, 1 - Player 2, 2 - No spawning droid.
  owner = property(getOwner)

  #\cond
  def getTurnsUntilAssembled(self):
    self.validify()
    return library.tileGetTurnsUntilAssembled(self._ptr)
  #\endcond
  ##The number of turns until a Droid is assembled.
  turnsUntilAssembled = property(getTurnsUntilAssembled)

  #\cond
  def getVariantToAssemble(self):
    self.validify()
    return library.tileGetVariantToAssemble(self._ptr)
  #\endcond
  ##The variant of Droid to assemble.
  variantToAssemble = property(getVariantToAssemble)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "owner: %s\n" % self.getOwner()
    ret += "turnsUntilAssembled: %s\n" % self.getTurnsUntilAssembled()
    ret += "variantToAssemble: %s\n" % self.getVariantToAssemble()
    return ret

##Represents Variant of Droid.
class ModelVariant(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.modelVariantGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.modelVariants:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  #\cond
  def getId(self):
    self.validify()
    return library.modelVariantGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getName(self):
    self.validify()
    return library.modelVariantGetName(self._ptr)
  #\endcond
  ##The name of this variant of Droid.
  name = property(getName)

  #\cond
  def getVariant(self):
    self.validify()
    return library.modelVariantGetVariant(self._ptr)
  #\endcond
  ##The ModelVariant specific id representing this variant of Droid.
  variant = property(getVariant)

  #\cond
  def getCost(self):
    self.validify()
    return library.modelVariantGetCost(self._ptr)
  #\endcond
  ##The scrap cost to spawn this Droid variant into the game.
  cost = property(getCost)

  #\cond
  def getMaxAttacks(self):
    self.validify()
    return library.modelVariantGetMaxAttacks(self._ptr)
  #\endcond
  ##The maximum number of times the Droid can attack.
  maxAttacks = property(getMaxAttacks)

  #\cond
  def getMaxHealth(self):
    self.validify()
    return library.modelVariantGetMaxHealth(self._ptr)
  #\endcond
  ##The maximum amount of this health this Droid can have
  maxHealth = property(getMaxHealth)

  #\cond
  def getMaxMovement(self):
    self.validify()
    return library.modelVariantGetMaxMovement(self._ptr)
  #\endcond
  ##The maximum number of moves this Droid can move.
  maxMovement = property(getMaxMovement)

  #\cond
  def getRange(self):
    self.validify()
    return library.modelVariantGetRange(self._ptr)
  #\endcond
  ##The range of this Droid's attack.
  range = property(getRange)

  #\cond
  def getAttack(self):
    self.validify()
    return library.modelVariantGetAttack(self._ptr)
  #\endcond
  ##The power of this Droid variant's attack.
  attack = property(getAttack)

  #\cond
  def getMaxArmor(self):
    self.validify()
    return library.modelVariantGetMaxArmor(self._ptr)
  #\endcond
  ##How much armor the Droid has which reduces damage taken.
  maxArmor = property(getMaxArmor)

  #\cond
  def getScrapWorth(self):
    self.validify()
    return library.modelVariantGetScrapWorth(self._ptr)
  #\endcond
  ##The amount of scrap the Droid drops.
  scrapWorth = property(getScrapWorth)

  #\cond
  def getTurnsToBeHacked(self):
    self.validify()
    return library.modelVariantGetTurnsToBeHacked(self._ptr)
  #\endcond
  ##The number of turns this unit will be hacked, if it is hacked. If 0, the droid cannot be hacked.
  turnsToBeHacked = property(getTurnsToBeHacked)

  #\cond
  def getHacketsMax(self):
    self.validify()
    return library.modelVariantGetHacketsMax(self._ptr)
  #\endcond
  ##The maximum number of hackets that can be sustained before hacked. If 0, the Droid cannot be hacked.
  hacketsMax = property(getHacketsMax)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "name: %s\n" % self.getName()
    ret += "variant: %s\n" % self.getVariant()
    ret += "cost: %s\n" % self.getCost()
    ret += "maxAttacks: %s\n" % self.getMaxAttacks()
    ret += "maxHealth: %s\n" % self.getMaxHealth()
    ret += "maxMovement: %s\n" % self.getMaxMovement()
    ret += "range: %s\n" % self.getRange()
    ret += "attack: %s\n" % self.getAttack()
    ret += "maxArmor: %s\n" % self.getMaxArmor()
    ret += "scrapWorth: %s\n" % self.getScrapWorth()
    ret += "turnsToBeHacked: %s\n" % self.getTurnsToBeHacked()
    ret += "hacketsMax: %s\n" % self.getHacketsMax()
    return ret
