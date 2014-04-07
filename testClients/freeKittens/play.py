__author__ = 'Tarnasa'

import random
import heapq

from tools import *
from cat_scan import *


def play(game):
    for kitten in game.kittens:
        for _ in xrange(kitten.maxMovement):
            possible_moves = [[kitten.x + x, kitten.y + y] for x, y in [[1, 0], [0, -1], [-1, 0], [0, 1]]
                              if inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1,
                              kitten.x + x, kitten.y + y) and
                              len(game.grid[kitten.x + x][kitten.y + y]) == 1]
            if possible_moves:
                x, y = random.choice(possible_moves)
                cat_move(game, kitten, x, y)

        if kitten.attack < 0:
            possible_toys = [playmate for playmate in game.kittens if
                             manhattan(playmate.x, playmate.y, kitten.x, kitten.y) <= kitten.range]
        else:
            possible_toys = [toy for toy in game.toys if manhattan(toy.x, toy.y, kitten.x, kitten.y) <= kitten.range]
        for _ in xrange(kitten.maxAttacks):
            if possible_toys:
                toy = random.choice(possible_toys)
                kitten.operate(toy.x, toy.y)


def play_fast(game):
    # Look for best toys
    ranked_toys = heapq.heapify([(toy.possible_health, toy) for toy in game.toys])

    pass