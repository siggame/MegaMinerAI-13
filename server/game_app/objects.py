import networking.config.config

cfgVariants = networking.config.config.readConfig("config/variants.cfg")

class Player(object):
  game_state_attributes = ['id', 'playerName', 'time', 'scrapAmount']
  def __init__(self, game, id, playerName, time, scrapAmount):
    self.game = game
    self.id = id
    self.playerName = playerName
    self.time = time
    self.scrapAmount = scrapAmount
    self.updatedAt = game.turnNumber
    self.dropsInProgress = [] # list: [tile, type, turnsUntilDrop] type:0-wall,1-turret
    self.assembleQueue = [] # List of new droid stats

  def toList(self):
    return [self.id, self.playerName, self.time, self.scrapAmount, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, scrapAmount = self.scrapAmount, )
  
  def nextTurn(self):
    if self.id == self.game.playerID:
      if self.scrapAmount > self.game.maxScrap:
        self.scrapAmount = self.game.maxScrap
      elif self.scrapAmount < 0:
        #badbadbadbadbadbad I love python's hashtag comments
        self.scrapAmount = 0

      # Spawn droids
      for newDroidStats in self.assembleQueue:
        newDroid = self.game.addObject(Droid, newDroidStats)
        self.game.grid[newDroid.x][newDroid.y].append(newDroid)
        self.game.grid[newDroid.x][newDroid.y][0].turnsUntilAssembled = 0
      self.assembleQueue = []

      # Update orbital drops
      # TODO: Decide whether droids are able to move onto dropzones
      for dropzone, dropType, turnsUntilDrop in self.dropsInProgress:
        turnsUntilDrop -= 1
        if turnsUntilDrop == 0:
          dropzone.turnsUntilAssembled = 0
          if len(self.game.grid[dropzone.x][dropzone.y]) > 1:
            # Kill droids on dropzone
            # TODO: Actually kill droid
            self.game.grid[dropzone.x][dropzone.y][1].health = 0
          if dropType == 0:
            dropzone.owner = 3
          if dropType == 1:
            variant = self.game.variantToModelVariant(4)
            # ['id', 'x', 'y', 'owner', 'variant', 'attacksLeft', 'maxAttacks', 'healthLeft', 'maxHealth', 'movementLeft', 'maxMovement', 'range', 'attack', 'armor', 'maxArmor', 'scrapWorth', 'hackedTurnsLeft', 'hackets']
            newDroidStats = [dropzone.x, dropzone.y, self.id, variant.variant, variant.maxAttacks, variant.maxAttacks, variant.maxHealth, variant.maxHealth, variant.maxMovement, variant.maxMovement, variant.range, variant.attack, variant.maxArmor, variant.maxArmor, variant.scrapWorth, 0, 0]
            newDroid = self.game.addObject(Droid, newDroidStats)
            self.game.grid[newDroid.x][newDroid.y].append(newDroid)
      # Remove finished drops
      self.dropsInProgress[:] = [[drop[0], drop[1], drop[2] - 1] for drop in self.dropsInProgress if drop[2] != 0]

    return True

  def talk(self, message):
    #make sure this never works properly
    pass

  def orbitalDrop(self, x, y, type):
    # type == 0 for wall
    # type == 1 for turret
    if not (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
      return 'Turn {}: You cannot drop onto a location off of the map. ({},{})'.format(self.game.turnNumber, x, y)
    if type != 0 and type != 1:
      return 'Turn {}: You cannot drop a structure of type {}. Must be 0 or 1.'.format(self.game.turnNumber, type)
    if type == 0:
      cost = self.game.wallCost
    else:
      cost = self.game.variantToModelVariant(4).cost
    if self.scrapAmount < cost:
      return 'Turn {}: You do not have enough scrap to drop. Have: () Need: ()'.format(self.game.turnNumber, self.scrapAmount, cost)
    tile = self.getTile(x, y)
    if tile.health > 0:
      return 'Turn {}: You cannot drop a structure onto another structure.'.format(self.game.turnNumber)
    if tile.turnsUntilAssembled > 0:
      return 'Turn {}: You cannot drop a structure onto a tile that is assembling a droid.'.format(self.game.turnNumber)
    
    if self.id == 0:
      xoff = 0
    else:
      xoff = self.game.mapWidth - 1

    turnsUntilDrop = 1 + (self.game.maxTurnsUntilDeploy - 1) * (abs(xoff - x) / float(self.game.mapWidth - 1))
    tile.turnsUntilAssembled = 1
    self.scrapAmount -= cost

    self.game.dropsInProgress.append([tile, type, turnsUntilDrop])

    return True

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
  game_state_attributes = ['id', 'x', 'y', 'owner', 'variant', 'attacksLeft', 'maxAttacks', 'healthLeft', 'maxHealth', 'movementLeft', 'maxMovement', 'range', 'attack', 'armor', 'maxArmor', 'scrapWorth', 'hackedTurnsLeft', 'hackets']
  def __init__(self, game, id, x, y, owner, variant, attacksLeft, maxAttacks, healthLeft, maxHealth, movementLeft, maxMovement, range, attack, armor, maxArmor, scrapWorth, hackedTurnsLeft, hackets):
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
    self.hackedTurnsLeft = hackedTurnsLeft
    self.hackets = hackets
    self.updatedAt = game.turnNumber

  #Distance for Taxicab Distance
  def taxiDist(self, source, x, y):
    return abs(source.x-x) + abs(source.y-y)

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.variant, self.attacksLeft, self.maxAttacks, self.healthLeft, self.maxHealth, self.movementLeft, self.maxMovement, self.range, self.attack, self.armor, self.maxArmor, self.scrapWorth, self.hackedTurnsLeft, self.hackets, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, variant = self.variant, attacksLeft = self.attacksLeft, maxAttacks = self.maxAttacks, healthLeft = self.healthLeft, maxHealth = self.maxHealth, movementLeft = self.movementLeft, maxMovement = self.maxMovement, range = self.range, attack = self.attack, armor = self.armor, maxArmor = self.maxArmor, scrapWorth = self.scrapWorth, hackedTurnsLeft = self.hackedTurnsLeft, hackets = self.hackets, )
  
  def nextTurn(self):
    pass

  def move(self, x, y):
    if self.owner != self.game.playerID and self.hackedTurnsLeft == 0:
      return 'Turn {}: You cannot use the other player\'s unit when it\'s not hacked {}. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.healthLeft <= 0:
      return 'Turn {}: Your unit {} does not have any health left. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.movementLeft <= 0:
      return 'Turn {}: Your unit {} does not have any movements left. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.owner == self.game.playerID and self.hackedTurnsLeft > 0:
      return 'Turn {}: You cannot use your unit while it\'s hacked {}. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif not (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
      return 'Turn {}: Your unit {} cannot move off the map. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif len(self.game.grid[x][y]) > 1:
      return 'Turn {}: Your unit {} is trying to run into something. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.game.getTile(x, y).health > 0 and self.game.getTile(x, y).owner != self.game.playerID:
      return 'Turn {}: Your unit {} is trying to run into either a wall or enemy base. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.game.getTile(x, y).isSpawning == 1:
      return 'Turn {}: Your unit {} is trying to move onto a spawn tile that is spawning a unit. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif abs(self.x-x) + abs(self.y-y) != 1:
      return 'Turn {}: Your unit {} can only move one unit away. ({}.{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)

    prevTile = self.game.getTile(self.x, self.y)

    self.game.grid[self.x][self.y].remove(self)

    self.game.addAnimation(MoveAnimation(self.id,self.x,self.y,x,y))
    self.x = x
    self.y = y
    self.movementLeft -= 1
    self.game.grid[self.x][self.y].append(self)


    tile = self.game.getTile(x, y)

    return True

  #the function to deal damage; separated out so armor damage can be changed
  def doDamage(self, attacker, target):
    damage = 3
    if target.armor > 0:
      damage = attacker.attack/target.armor
      target.armor -= attacker.attack
      if target.armor < 0:
        target.armor = 0
    else:
      damage = attacker.attack

    target.health -= damage

  def operate(self, target):
    variantName = self.game.variantString[self.variant]
    #make sure valid for operating on either a droid or tile
    if isinstance(target, Droid) or isinstance(target, Tile):
      return "Turn %i: You can only attack droids/hangars or heal tiles."%(self.game.turnNumber)
    elif self.owner == self.game.playerID and self.hackedTurnsLeft > 0:
      return "Turn %i: You cannot control your %s while it is hacked."%(self.game.turnNumber, variantName)
    elif self.attacksLeft == 0:
      return "Turn %i: Your %s has no attacks left."%(self.game.turnNumber, variantName)
    elif self.healthLeft < 0:
      return "Turn %i: Your %s does not have any health left."%(self.game.turnNumber, variantName)

    #separate this out so it makes more sense/easier to change
    hackerVariantVal = 3

    if isinstance(target, Droid):
      #droid logic here
      opponentName = self.game.variantString[target.variant]
      if self.owner != self.game.playerID and self.hackedTurnsLeft <= 0:
        return "Turn %i: You cannot control your opponent's %s when it isn't hacked."%(self.game.turnNumber, opponentName)
      elif self.attack < 0 and target.owner != self.game.playerID:
        return "Turn %i: Your %s cannot heal your opponent's %s."%(self.game.turnNumber, variantName, opponentName)
      elif self.taxiDist(self, target.x, target.y) > self.range:
        return "Turn %i: The opponent's %s is too far away from your %s."%(self.game.turnNumber, opponentName, variantName)
      elif self.attack > 0 and target.owner == self.game.playerID:
       return "Turn %i: Your %s cannot attack your %s."%(self.game.turnNumber, variantName, opponentName)

      if self.attack < 0:
        #heal the armor by the attack amount [attack is negative, subtracting will increase]
        target.armor -= self.attack
        if target.armor > target.maxArmor:
          target.armor = target.maxArmor
        #reduce hackets [Attack is negative, adding will decrease]
        target.hackets += self.attack
        if target.hackets < 0:
          target.hackets = 0
      elif self.attack > 0 and self.variant != hackerVariantVal:
        self.doDamage(self, target)
      elif self.attack > 0 and self.variant == hackerVariantVal:
        target.hackets += self.attack
        if target.hackets > self.game.maxHackets:
          target.hackedTurnsLeft = self.game.turnsToBeHacked

    elif isinstance(target, Tile):
      #tile logic here
      if self.variant == hackerVariantVal:
        return "Turn %i: Your %s cannot attack walls."%(self.game.turnNumber, variantName)
      elif target.health <= 0:
        return "Turn %i: Your %s can only operate on walls or hangars."%(self.game.turnNumber, variantName)
      elif target.owner == self.game.playerID and self.attack > 0:
        return "Turn %i: Your %s cannot attack your own hangar."%(self.game.turnNumber, variantName)
      elif target.owner != self.game.playerID and self.attack < 0:
        return "Turn %i: Your %s cannot heal the opponent's hangar."%(self.game.turnNumber, variantName)
      elif self.attack < 0:
        #heal the wall
        target.health -= self.attack
        if target.health > self.game.maxWallHealth:
          target.health = self.game.maxWallHealth
      elif self.attack > 0:
        target.health -= self.attack

    pass


  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class Tile(Mappable):
  game_state_attributes = ['id', 'x', 'y', 'owner', 'turnsUntilAssembled', 'scrapAmount', 'health']
  def __init__(self, game, id, x, y, owner, turnsUntilAssembled, scrapAmount, health):
    self.game = game
    self.id = id
    self.x = x
    self.y = y
    self.owner = owner
    self.turnsUntilAssembled = turnsUntilAssembled
    self.scrapAmount = scrapAmount
    self.health = health
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.turnsUntilAssembled, self.scrapAmount, self.health, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, turnsUntilAssembled = self.turnsUntilAssembled, scrapAmount = self.scrapAmount, health = self.health, )
  
  def nextTurn(self):
    pass

  def assemble(self, type):
    player = self.game.objects.players[self.game.playerID]

    #make sure turret isn't being assembled
    turretVariantNum = 4

    if type == turretVariantNum:
      return 'Turn {}: You cannot assemble a turret; use orbital drop.'.format(self.game.turnNumber)
    if self.owner != self.game.playerID:
      return 'Turn {}: You cannot assemble a droid on a non hanger tile. ({},{})'.format(self.game.turnNumber, self.x, self.y)
    if len(self.game.grid[self.x][self.y]) > 1:
      return 'Turn {} You cannot assemble a droid on top of another droid. ({},{})'.format(self.game.turnNumber, self.x, self.y)
    if self.turnsUntilAssembled != 0:
       return 'Turn {} You cannot assemble a droid because you are already attempting to assemble here ({},{})'.format(self.game.turnNumber, self.x, self.y)
    count = len([droid for droid in self.game.objects.droids if droid.owner == self.playerID])
    if count >= self.game.maxDroids:
      return 'Turn {} You cannot assemble a droid because you already have the maximum number of droids ({})'.format(self.game.turnNumber, self.game.maxDroids)
    variant = self.game.variantToModelVariant(type)
    if variant is None:
      return 'Turn {}: You cannot spawn a droid with this variant ({}).'.format(self.game.turnNumber, type)
    if player.scrapAmount < variant.cost:
      return 'Turn {}: You do not have enough resources({}) to spawn this unit({}).'.format(self.game.turnNumber, player.scrapAmount, variant.cost)

    player.scrapAmount -= variant.cost

    # ['id', 'x', 'y', 'owner', 'variant', 'attacksLeft', 'maxAttacks', 'healthLeft', 'maxHealth', 'movementLeft', 'maxMovement', 'range', 'attack', 'armor', 'maxArmor', 'scrapWorth', 'hackedTurnsLeft', 'hackets']
    newDroidStats = [self.x, self.y, self.owner, type, variant.maxAttacks, variant.maxAttacks, variant.maxHealth, variant.maxHealth, variant.maxMovement, variant.maxMovement, variant.range, variant.attack, variant.maxArmor, variant.maxArmor, variant.scrapWorth, 0, 0]
    player.assembleQueue.append(newDroidStats)
    self.turnsUntilAssembled = 1

    # NOTE: we are providing 0 for droid.id
    self.game.addAnimation(SpawnAnimation(self.id, 0))

    return True

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

class ModelVariant(object):
  game_state_attributes = ['id', 'name', 'variant', 'cost', 'maxAttacks', 'maxHealth', 'maxMovement', 'range', 'attack', 'maxArmor', 'scrapWorth']
  def __init__(self, game, id, name, variant, cost, maxAttacks, maxHealth, maxMovement, range, attack, maxArmor, scrapWorth):
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
    self.updatedAt = game.turnNumber

  def toList(self):
    return [self.id, self.name, self.variant, self.cost, self.maxAttacks, self.maxHealth, self.maxMovement, self.range, self.attack, self.maxArmor, self.scrapWorth, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, name = self.name, variant = self.variant, cost = self.cost, maxAttacks = self.maxAttacks, maxHealth = self.maxHealth, maxMovement = self.maxMovement, range = self.range, attack = self.attack, maxArmor = self.maxArmor, scrapWorth = self.scrapWorth, )
  
  def nextTurn(self):
    pass

  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)


# The following are animations and do not need to have any logic added
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

class AttackAnimation:
  def __init__(self, actingID, targetID):
    self.actingID = actingID
    self.targetID = targetID

  def toList(self):
    return ["attack", self.actingID, self.targetID, ]

  def toJson(self):
    return dict(type = "attack", actingID = self.actingID, targetID = self.targetID)

class SpawnAnimation:
  def __init__(self, sourceID, unitID):
    self.sourceID = sourceID
    self.unitID = unitID

  def toList(self):
    return ["spawn", self.sourceID, self.unitID, ]

  def toJson(self):
    return dict(type = "spawn", sourceID = self.sourceID, unitID = self.unitID)

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

class RepairAnimation:
  def __init__(self, actingID, targetID):
    self.actingID = actingID
    self.targetID = targetID

  def toList(self):
    return ["repair", self.actingID, self.targetID, ]

  def toJson(self):
    return dict(type = "repair", actingID = self.actingID, targetID = self.targetID)

