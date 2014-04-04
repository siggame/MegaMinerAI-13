__author__ = 'Tarnasa'

import random

def play(game):
  for kitten in game.droids:
    if kitten.owner == game.getPlayerID():
      for _ in xrange(kitten.maxMovement):
        xoff, yoff = random.choice([[0, 1], [1, 0], [0, -1], [-1, 0]])
        kitten.move(kitten.x + xoff, kitten.y + yoff)
      