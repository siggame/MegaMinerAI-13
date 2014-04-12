__author__ = 'Tarnasa'

import random


def make_kittens_random(game):
    owner = game.players[game.playerID]
    if random.random() > 0.5:
        cattery = random.choice(game.tiles)
        if (len(game.grid[cattery.x][cattery.y]) == 1 or game.grid[cattery.x][cattery.y][1].variant != 7) and \
                cattery.turnsUntilAssembled == 0:
            breed = random.choice(game.modelVariants)
            if breed.variant != 7 and owner.scrapAmount >= breed.cost:
                owner.orbitalDrop(cattery.x, cattery.y, breed.variant)


def make_kittens_back(game):
    owner = game.players[game.playerID]
    if random.random() > 0.5:
        cattery_y = random.randint(0, game.mapHeight - 1)
        cattery_x = game.playerID * (game.mapWidth - 1)
        cattery = game.grid[cattery_x][cattery_y]
        if len(cattery) == 1 or cattery[1].variant != 7 and cattery[0].turnsUntilAssembled == 0:
            breed = game.modelVariants[random.choice([0, 1, 6])]
            if owner.scrapAmount >= breed.cost:
                owner.orbitalDrop(cattery_x, cattery_y, breed.variant)
