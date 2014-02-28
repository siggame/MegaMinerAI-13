# -*- coding: iso-8859-1 -*-
from structures import *

aspects = ['timer']

gameName = "Droids"

constants = [
  ]

modelOrder = ['Player', 'Mappable', 'Droid', 'Tile', 'ModelVariant']

globals = [
  Variable('mapWidth', int, 'The width of the total map.'),
  Variable('mapHeight', int, 'The height of the total map.'),
  Variable('turnNumber', int, 'The current turn number.'),
  Variable('maxDroids', int, 'The maximum number of Droids allowed per player.'),
  Variable('maxWalls', int, 'The maximum number of walls allowed per player.'),
  Variable('playerID', int, 'The id of the current player.'),
  Variable('gameNumber', int, 'What number game this is for the server.'),
  Variable('scrapRate', int, 'The rate a player receives scrap per turn.'),
  Variable('maxScrap', int, 'The maximum amount of scrap a player can have at once.')
]

playerData = [
  Variable('scrapAmount', int, 'The amount of scrap you have in your Hangar.'),
  ]

playerFunctions = [
  Function('talk', [Variable('message', str)], doc='Allows a player to display messages on the screen'),
  Function('orbitalDrop', [Variable('x', int), Variable('y', int), Variable('type', int)], doc='Allows a player to spawn a structure.'),
]

#MAPPABLE
Mappable = Model('Mappable',
  data=[
    Variable('x', int, 'X position of the object'),
    Variable('y', int, 'Y position of the object')
  ],
  doc='A mappable object!',
)

#TILE
Tile = Model('Tile',
  parent = Mappable,
  data = [
    Variable('owner', int, 'The owner of the tile. If 0: Player 1; If 1: Player 2; '),
    Variable('turnsUntilAssembled', int, 'The number of turns until a structure is assembled.'),
    Variable('scrapAmount', int, 'The amount of scrap on this tile.'),
    Variable('health', int, 'The health of the Hangar or Wall on this tile.')

    ],
  functions=[
    Function('assemble',[Variable('type',int)],
    doc='Attempt to assemble a Droid at this location.'),
    ],
  doc='Represents a single tile on the map.',
  permanent = True,
  )

#DROID
Droid = Model('Droid',
  parent = Mappable,
  data = [
    Variable('owner', int, 'The owner of this Droid.'),
    Variable('variant', int, 'The variant of this Droid. This variant refers to list of DroidVariants.'),
    Variable('attacksLeft', int, 'The number of attacks the Droid has remaining.'),
    Variable('maxAttacks', int, 'The maximum number of times the Droid can attack.'),
    Variable('healthLeft', int, 'The current amount health this Droid has remaining.'),
    Variable('maxHealth', int, 'The maximum amount of this health this Droid can have'),
    Variable('movementLeft', int, 'The number of moves this Droid has remaining.'),
    Variable('maxMovement', int, 'The maximum number of moves this Droid can move.'),
    Variable('range', int, 'The range of this Droid\'s attack.'),
    Variable('attack', int, 'The power of this Droid variant\'s attack.'),
    Variable('armor', int, 'How much armor the Droid has which reduces damage taken.'),
    Variable('maxArmor', int, 'How much armor the Droid has which reduces damage taken.'),
    Variable('scrapWorth', int, 'The amount of scrap the Droid drops.'),
    Variable('hackedTurnsLeft', int, 'The number of turns the Droid has remaining as hacked.'),
    Variable('hackets', int, 'The amount of hacking progress that has been made.')
    ],
  doc='Represents a single Droid on the map.',
    functions=[
    Function('move',[Variable('x', int), Variable('y', int)],
    doc='Make the Droid move to the respective x and y location.'),
    ],

  )

Droid.addFunctions([Function("operate", [ Variable("target", Droid)],
    doc='Command to operate (repair, attack, hack) on another Droid.')])

#MODELVARIANT
ModelVariant = Model('ModelVariant',
  data = [
    Variable('name', str, 'The name of this variant of Droid.'),
    Variable('variant', int, 'The ModelVariant specific id representing this variant of Droid.'),
    Variable('cost', int, 'The scrap cost to spawn this Droid variant into the game.'),
    Variable('maxAttacks', int, 'The maximum number of times the Droid can attack.'),
    Variable('maxHealth', int, 'The maximum amount of this health this Droid can have'),
    Variable('maxMovement', int, 'The maximum number of moves this Droid can move.'),
    Variable('range', int, 'The range of this Droid\'s attack.'),
    Variable('attack', int, 'The power of this Droid variant\'s attack.'),
    Variable('maxArmor', int, 'How much armor the Droid has which reduces damage taken.'),
    Variable('scrapWorth', int, 'The amount of scrap the Droid drops.')
    ],
  doc='Represents Variant of Droid.',
  functions=[],
  permanent = True,
  )

move = Animation('move',
  data=[
    Variable('actingID', int),
    Variable('fromX', int),
    Variable('fromY', int),
    Variable('toX', int),
    Variable('toY', int)
  ],
  )

attack = Animation('attack',
  data=[
    Variable('actingID', int),
    Variable('targetID', int)
  ],
  )

repair = Animation('repair',
  data=[
    Variable('actingID', int),
    Variable('targetID', int)
  ],
  )

hack = Animation('hack',
  data=[
    Variable('actingID', int),
    Variable('targetID', int)
  ],
  )

spawn = Animation('spawn',
  data=[
    Variable('sourceID', int),
    Variable('unitID', int)
  ],
  )

orbitalDrop = Animation('orbitalDrop',
  data=[
    Variable('sourceID', int)
  ],
  )
