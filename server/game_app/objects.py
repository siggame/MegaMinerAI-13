class Player(object):
  game_state_attributes = ['id', 'playerName', 'time', 'scrapAmount']
  def __init__(self, game, id, playerName, time, scrapAmount):
    self.game = game
    self.id = id
    self.playerName = playerName
    self.time = time
    self.scrapAmount = scrapAmount
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.playerName, self.time, self.scrapAmount, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, scrapAmount = self.scrapAmount, )
  
  def nextTurn(self):
    pass

  def talk(self, message):
    pass

  def orbitalDrop(self, x, y, variant):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Mappable(object):
  game_state_attributes = ['id', 'x', 'y']
  def __init__(self, game, id, x, y):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, )
  
  def nextTurn(self):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Droid(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'variant', 'attacksLeft', 'maxAttacks', 'healthLeft', 'maxHealth', 'movementLeft', 'maxMovement', 'range', 'attack', 'armor', 'maxArmor', 'scrapWorth', 'turnsToBeHacked', 'hackedTurnsLeft', 'hackets', 'hacketsMax']
  def __init__(self, game, id, x, y, owner, variant, attacksLeft, maxAttacks, healthLeft, maxHealth, movementLeft, maxMovement, range, attack, armor, maxArmor, scrapWorth, turnsToBeHacked, hackedTurnsLeft, hackets, hacketsMax):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.variant = variant
    self.attacksLeft = attacksLeft
    self.maxAttacks = maxAttacks
    self.healthLeft = healthLeft
    self.maxHealth = maxHealth
    self.movementLeft = movementLeft
    self.maxMovement = maxMovement
    self.range = range
    self.attack = attack
    self.armor = armor
    self.maxArmor = maxArmor
    self.scrapWorth = scrapWorth
    self.turnsToBeHacked = turnsToBeHacked
    self.hackedTurnsLeft = hackedTurnsLeft
    self.hackets = hackets
    self.hacketsMax = hacketsMax
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.variant, self.attacksLeft, self.maxAttacks, self.healthLeft, self.maxHealth, self.movementLeft, self.maxMovement, self.range, self.attack, self.armor, self.maxArmor, self.scrapWorth, self.turnsToBeHacked, self.hackedTurnsLeft, self.hackets, self.hacketsMax, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, variant = self.variant, attacksLeft = self.attacksLeft, maxAttacks = self.maxAttacks, healthLeft = self.healthLeft, maxHealth = self.maxHealth, movementLeft = self.movementLeft, maxMovement = self.maxMovement, range = self.range, attack = self.attack, armor = self.armor, maxArmor = self.maxArmor, scrapWorth = self.scrapWorth, turnsToBeHacked = self.turnsToBeHacked, hackedTurnsLeft = self.hackedTurnsLeft, hackets = self.hackets, hacketsMax = self.hacketsMax, )
  
  def nextTurn(self):
    pass

  def move(self, x, y):
    pass

  def operate(self, x, y):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Tile(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'turnsUntilAssembled', 'variantToAssemble']
  def __init__(self, game, id, x, y, owner, turnsUntilAssembled, variantToAssemble):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.turnsUntilAssembled = turnsUntilAssembled
    self.variantToAssemble = variantToAssemble
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.turnsUntilAssembled, self.variantToAssemble, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, turnsUntilAssembled = self.turnsUntilAssembled, variantToAssemble = self.variantToAssemble, )
  
  def nextTurn(self):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class ModelVariant(object):
  game_state_attributes = ['id', 'name', 'variant', 'cost', 'maxAttacks', 'maxHealth', 'maxMovement', 'range', 'attack', 'maxArmor', 'scrapWorth', 'turnsToBeHacked', 'hacketsMax']
  def __init__(self, game, id, name, variant, cost, maxAttacks, maxHealth, maxMovement, range, attack, maxArmor, scrapWorth, turnsToBeHacked, hacketsMax):
    self.game = game
    self.id = id
    self.name = name
    self.variant = variant
    self.cost = cost
    self.maxAttacks = maxAttacks
    self.maxHealth = maxHealth
    self.maxMovement = maxMovement
    self.range = range
    self.attack = attack
    self.maxArmor = maxArmor
    self.scrapWorth = scrapWorth
    self.turnsToBeHacked = turnsToBeHacked
    self.hacketsMax = hacketsMax
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.name, self.variant, self.cost, self.maxAttacks, self.maxHealth, self.maxMovement, self.range, self.attack, self.maxArmor, self.scrapWorth, self.turnsToBeHacked, self.hacketsMax, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, name = self.name, variant = self.variant, cost = self.cost, maxAttacks = self.maxAttacks, maxHealth = self.maxHealth, maxMovement = self.maxMovement, range = self.range, attack = self.attack, maxArmor = self.maxArmor, scrapWorth = self.scrapWorth, turnsToBeHacked = self.turnsToBeHacked, hacketsMax = self.hacketsMax, )
  
  def nextTurn(self):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)


# The following are animations and do not need to have any logic added
class SpawnAnimation:
  def __init__(self, sourceID, unitID):
    self.sourceID = sourceID
    self.unitID = unitID

  def toList(self):
    return ["spawn", self.sourceID, self.unitID, ]

  def toJson(self):
    return dict(type = "spawn", sourceID = self.sourceID, unitID = self.unitID)

class RepairAnimation:
  def __init__(self, actingID, targetID):
    self.actingID = actingID
    self.targetID = targetID

  def toList(self):
    return ["repair", self.actingID, self.targetID, ]

  def toJson(self):
    return dict(type = "repair", actingID = self.actingID, targetID = self.targetID)

class MoveAnimation:
  def __init__(self, actingID, fromX, fromY, toX, toY):
    self.actingID = actingID
    self.fromX = fromX
    self.fromY = fromY
    self.toX = toX
    self.toY = toY

  def toList(self):
    return ["move", self.actingID, self.fromX, self.fromY, self.toX, self.toY, ]

  def toJson(self):
    return dict(type = "move", actingID = self.actingID, fromX = self.fromX, fromY = self.fromY, toX = self.toX, toY = self.toY)

class HackAnimation:
  def __init__(self, actingID, targetID):
    self.actingID = actingID
    self.targetID = targetID

  def toList(self):
    return ["hack", self.actingID, self.targetID, ]

  def toJson(self):
    return dict(type = "hack", actingID = self.actingID, targetID = self.targetID)

class OrbitalDropAnimation:
  def __init__(self, sourceID):
    self.sourceID = sourceID

  def toList(self):
    return ["orbitalDrop", self.sourceID, ]

  def toJson(self):
    return dict(type = "orbitalDrop", sourceID = self.sourceID)

class AttackAnimation:
  def __init__(self, actingID, targetID):
    self.actingID = actingID
    self.targetID = targetID

  def toList(self):
    return ["attack", self.actingID, self.targetID, ]

  def toJson(self):
    return dict(type = "attack", actingID = self.actingID, targetID = self.targetID)

