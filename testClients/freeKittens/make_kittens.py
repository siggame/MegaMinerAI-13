__author__ = 'Tarnasa'

import random


def make_kittens(game):
    owner = game.players[game.playerID]
    if random.random() > 0.5:
        cattery = random.choice(game.tiles)
        if (len(game.grid[cattery.x][cattery.y]) == 1 or game.grid[cattery.x][cattery.y][1].variant != 7) and \
                cattery.turnsUntilAssembled == 0:
            breed = random.choice(game.modelVariants)
            if breed.variant != 7 and owner.scrapAmount >= breed.cost:
                owner.orbitalDrop(cattery.x, cattery.y, breed.variant)