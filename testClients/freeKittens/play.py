__author__ = 'Tarnasa'

import random

from tools import *
from catscan import *


def play(game):
    toys = [toy for toy in game.droids if toy.owner != (game.playerID ^ toy.hackedTurnsLeft > 0)]
    kittens = [kitten for kitten in game.droids if kitten.owner == (game.playerID ^ kitten.hackedTurnsLeft > 0)]

    for kitten in kittens:
        for _ in xrange(kitten.maxMovement):
            possible_moves = [[kitten.x + x, kitten.y + y] for x, y in [[1, 0], [0, -1], [-1, 0], [0, 1]]
                              if inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1,
                              kitten.x + x, kitten.y + y) and
                              len(game.grid[kitten.x + x][kitten.y + y]) == 1]
            if possible_moves:
                x, y = random.choice(possible_moves)
                cat_move(game, kitten, x, y)

        if kitten.attack < 0:
            possible_toys = [playmate for playmate in kittens if
                             manhattan(playmate.x, playmate.y, kitten.x, kitten.y) <= kitten.range]
        else:
            possible_toys = [toy for toy in toys if manhattan(toy.x, toy.y, kitten.x, kitten.y) <= kitten.range]
        for _ in xrange(kitten.maxAttacks):
            if possible_toys:
                toy = random.choice(possible_toys)
                kitten.operate(toy.x, toy.y)