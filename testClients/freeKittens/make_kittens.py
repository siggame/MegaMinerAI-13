__author__ = 'Tarnasa'

import random

def make_kittens(game):
  if random.random() > 0.5:
    for cattery in game.tiles:
      if cattery.owner == game.getPlayerID() and cattery.type == 2 and random.random() > 0.8:
        breed = random.choice(game.modelVariants)
        if game.players[game.getPlayerID()].scrapAmount >= breed.cost:
          if cattery.assemble(breed.variant):
            break

