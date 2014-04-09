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
    self.dropsInProgress = [] # list of tiles
    self.assembleQueue = [] # List of new droid stats

  def toList(self):
    return [self.id, self.playerName, self.time, self.scrapAmount, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, playerName = self.playerName, time = self.time, scrapAmount = self.scrapAmount, )

  def nextTurn(self):
    #give scrap on first turn; wasn't working in startGame
    if self.game.turnNumber == 0:
      self.scrapAmount = self.game.maxScrap/2

    if self.id == self.game.playerID:
      self.scrapAmount += self.game.scrapRate

      if self.scrapAmount > self.game.maxScrap:
        self.scrapAmount = self.game.maxScrap
      elif self.scrapAmount < 0:
        #badbadbadbadbadbad I love python's hashtag comments
        self.scrapAmount = 0

      # Update orbital drops
      for dropzone in self.dropsInProgress:
        dropzone.turnsUntilAssembled -= 1
        if dropzone.turnsUntilAssembled <= 0:
          dropzone.owner = 2
          if len(self.game.grid[dropzone.x][dropzone.y]) > 1:
            # Kill droids on dropzone
            self.game.grid[dropzone.x][dropzone.y][1].healthLeft = 0
            self.game.grid[dropzone.x][dropzone.y][1].handleDeath()
          variant = self.game.variantToModelVariant(dropzone.variantToAssemble)
          # ['id', 'x', 'y', 'owner', 'variant', 'attacksLeft', 'maxAttacks', 'healthLeft', 'maxHealth', 'movementLeft', 'maxMovement', 'range', 'attack', 'armor', 'maxArmor', 'scrapWorth', 'hackedTurnsLeft', 'hackets']
          # ['id', 'x', 'y', 'owner', 'variant', 'attacksLeft', 'maxAttacks', 'healthLeft', 'maxHealth', 'movementLeft', 'maxMovement', 'range', 'attack', 'armor', 'maxArmor', 'scrapWorth', 'turnsToBeHacked', 'hackedTurnsLeft', 'hackets', 'hacketsMax']
          newDroidStats = [dropzone.x, dropzone.y, self.id, variant.variant, variant.maxAttacks, variant.maxAttacks, variant.maxHealth, variant.maxHealth, variant.maxMovement, variant.maxMovement, variant.range, variant.attack, variant.maxArmor, variant.maxArmor, variant.scrapWorth, variant.turnsToBeHacked, 0, 0, variant.hacketsMax]
          newDroid = self.game.addObject(Droid, newDroidStats)
          self.game.grid[newDroid.x][newDroid.y].append(newDroid)
      # Remove finished drops
      self.dropsInProgress[:] = [drop for drop in self.dropsInProgress if drop.turnsUntilAssembled != 0]

    return True

  def talk(self, message):
    #make sure this never works properly
    pass

  def orbitalDrop(self, x, y, variant):
    HangarVariant = 7
    if not (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
      return 'Turn {}: You cannot drop onto a location off of the map. ({},{})'.format(self.game.turnNumber, x, y)
    if variant == HangarVariant:
      return 'Turn {}: You cannot drop a Hangar.'.format(self.game.turnNumber)
    variantCheck = self.game.variantToModelVariant(variant)
    if variantCheck is None:
      return 'Turn {}: {} is not a valid variant number.'.format(self.game.turnNumber, variant)
    cost = self.game.variantToModelVariant(variant).cost
    if self.scrapAmount < cost:
      return 'Turn {}: You do not have enough scrap to drop. Have: {} Need: {}'.format(self.game.turnNumber, self.scrapAmount, cost)
    tile = self.game.getTile(x, y)
    if tile.turnsUntilAssembled > 0:
      return 'Turn {}: You cannot drop a droid onto a tile that is assembling a droid.'.format(self.game.turnNumber)
    if len(self.game.grid[x][y]) > 1:
      if self.game.grid[x][y][1].variant == HangarVariant:
        return 'Turn {}: You cannot drop a droid onto a hangar'.format(self.game.turnNumber)

    xoff = -1
    if self.id == 1:
      xoff = self.game.mapWidth

    #turnsUntilDrop = 1 + (self.game.maxTurnsUntilDeploy - 1) * (abs(xoff - x) / float(self.game.mapWidth - 1))
    turnsUntilDrop = abs(xoff - x) * self.game.dropTime
    tile.turnsUntilAssembled = turnsUntilDrop
    tile.variantToAssemble = variant
    self.scrapAmount -= cost

    #change owner
    tile.owner = self.id

    self.dropsInProgress.append(tile)

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

  #Distance for Taxicab Distance
  def taxiDist(self, source, x, y):
    return abs(source.x-x) + abs(source.y-y)

  def toList(self):
    return [self.id, self.x, self.y, self.owner, self.variant, self.attacksLeft, self.maxAttacks, self.healthLeft, self.maxHealth, self.movementLeft, self.maxMovement, self.range, self.attack, self.armor, self.maxArmor, self.scrapWorth, self.turnsToBeHacked, self.hackedTurnsLeft, self.hackets, self.hacketsMax, ]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(id = self.id, x = self.x, y = self.y, owner = self.owner, variant = self.variant, attacksLeft = self.attacksLeft, maxAttacks = self.maxAttacks, healthLeft = self.healthLeft, maxHealth = self.maxHealth, movementLeft = self.movementLeft, maxMovement = self.maxMovement, range = self.range, attack = self.attack, armor = self.armor, maxArmor = self.maxArmor, scrapWorth = self.scrapWorth, turnsToBeHacked = self.turnsToBeHacked, hackedTurnsLeft = self.hackedTurnsLeft, hackets = self.hackets, hacketsMax = self.hacketsMax, )

  def handleDeath(self):
    if self.healthLeft <= 0:
      # Transfer scrap
      if self.x < self.game.mapWidth / 2:
        playerNum = 0
      else:
        playerNum = 1
      self.game.objects.players[playerNum].scrapAmount += self.scrapWorth
      if self.game.objects.players[playerNum].scrapAmount > self.game.maxScrap:
        self.game.objects.players[playerNum].scrapAmont = self.game.maxScrap
      self.game.grid[self.x][self.y].remove(self)
      self.game.removeObject(self)
      #This is actually a death animation, shhhhhhhhhh
      self.game.addAnimation(OrbitalDropAnimation(self.id))

  def nextTurn(self):
    if self.owner == (self.game.playerID ^ (self.hackedTurnsLeft > 0)):
      self.movementLeft = self.maxMovement
      self.attacksLeft = self.maxAttacks

      # This droid is hacked
      if self.hackedTurnsLeft > 0:
        self.hackedTurnsLeft -= 1
      # This droid is being hacked
      elif self.hackets > 0:
        self.hackets -= 1 # Hackets gradually decrease (ANTIVIRUS FTW)


    return True

  def move(self, x, y):
    if self.owner != (self.game.playerID ^ (self.hackedTurnsLeft > 0)):
      return 'Turn {}: You cannot use the other player\'s droid when it\'s not hacked {}. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.healthLeft <= 0:
      return 'Turn {}: Your droid {} does not have any health left. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.movementLeft <= 0:
      return 'Turn {}: Your droid {} does not have any movement left. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif not (0 <= x < self.game.mapWidth) or not (0 <= y < self.game.mapHeight):
      return 'Turn {}: Your droid {} cannot move off the map. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif len(self.game.grid[x][y]) > 1:
      return 'Turn {}: Your droid {} is trying to run into something. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif abs(self.x-x) + abs(self.y-y) != 1:
      return 'Turn {}: Your droid {} can only move one unit away. ({}.{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)

    self.game.grid[self.x][self.y].remove(self)

    self.game.addAnimation(MoveAnimation(self.id,self.x,self.y,x,y))
    self.x = x
    self.y = y
    self.movementLeft -= 1
    self.game.grid[self.x][self.y].append(self)

    return True

  #the function to deal damage; separated out so armor damage can be changed
  def doDamage(self, attacker, target):
    damage = 3
    if target.armor > 0:
      damage = int(attacker.attack * ((target.maxArmor - target.armor) / float(target.maxArmor)))
      target.armor -= attacker.attack
      if target.armor < 0:
        target.armor = 0
    else:
      damage = attacker.attack

    target.healthLeft -= damage
    #handle death
    if target.healthLeft <= 0:
      target.handleDeath()

  def operate(self, x, y):
    variantName = self.game.variantStrings[self.variant]
    #make sure valid for operating on either a droid or tile
    if not (0 <= x < self.game.mapWidth and 0 <= y < self.game.mapHeight):
      return "Turn %i: You may only operate in-bounds."%(self.game.turnNumber)
    elif self.owner != (self.game.playerID ^ (self.hackedTurnsLeft > 0)):
      return 'Turn {}: You cannot use the other player\'s droid when it\'s not hacked {}. ({},{}) -> ({},{})'.format(self.game.turnNumber, self.id, self.x, self.y, x, y)
    elif self.attacksLeft == 0:
      return "Turn %i: Your %s has no attacks left."%(self.game.turnNumber, variantName)
    elif self.healthLeft <= 0:
      return "Turn %i: Your %s does not have any health left."%(self.game.turnNumber, variantName)

    #separate this out so it makes more sense/easier to change
    hackerVariantVal = 3
    wall = 5
    hangar = 7

    targetId = None

    #length of 2 = droid on tile
    if len(self.game.grid[x][y]) == 2:
      target = self.game.grid[x][y][1]
      targetId = target.id
      #droid logic here
      opponentName = self.game.variantStrings[target.variant]
      if self.attack < 0 and target.owner != (self.game.playerID ^ (target.hackedTurnsLeft > 0)):
        return "Turn %i: Your %s cannot heal the %s."%(self.game.turnNumber, variantName, opponentName)
      elif self.taxiDist(self, target.x, target.y) > self.range:
        return "Turn %i: The opponent's %s is too far away from your %s."%(self.game.turnNumber, opponentName, variantName)
      elif self.variant == hackerVariantVal and target.hackedTurnsLeft > 0 and target.owner == self.game.playerID:
        return "Turn %i: Your %s cannot operate on your %s."%(self.game.turnNumber, variantName, opponentName)
      elif self.attack > 0 and target.owner == (self.game.playerID ^ (target.hackedTurnsLeft > 0)):
        return "Turn %i: Your %s cannot operate on the %s."%(self.game.turnNumber, variantName, opponentName)
      elif self.variant == hackerVariantVal and (target.variant == wall or target.variant == hangar):
        return "Turn %i: Your %s cannot operate on a wall or a hangar"%(self.game.turnNumber, variantName)

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
        if target.hackets >= target.hacketsMax:
          target.hackedTurnsLeft = target.turnsToBeHacked
          target.hackets = 0

    else:
      return "Turn %i: Your %s cannot operate on an empty tile."%(self.game.turnNumber, variantName)

    self.attacksLeft -= 1
    if self.attack > 0 and self.variant != hackerVariantVal:
      self.game.addAnimation(AttackAnimation(self.id, targetId))
    elif self.attack > 0:
      self.game.addAnimation(HackAnimation(self.id, targetId))
    else:
      self.game.addAnimation(RepairAnimation(self.id, targetId))

    return True


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
    #Decrease Turns Until Assembled
    #if self.turnsUntilAssembled > 1:
    #  self.turnsUntilAssembled -= 1
    #Add To Spawn List If About To Spawn
    #elif self.turnsUntilAssembled == 1:
    #    pass
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

