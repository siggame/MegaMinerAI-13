__author__ = 'Tarnasa'

import random


def make_kittens(game):
    owner = game.players[game.playerID]
    if random.random() > 0.5:
        cattery = random.choice(game.tiles)
        breed = random.choice(game.modelVariants)
        owner.orbitalDrop(cattery.x, cattery.y, breed.variant)