__author__ = 'Tarnasa'

import random

def make_kittens(game):
  if random.random() > 0.5:
    cattery = game.tiles(random.randint(0, game.getMapWidth() * game.getMapHeight()))
    breed = random.choice(game.modelVariants)
    cattery.assemble(breed.variant)

