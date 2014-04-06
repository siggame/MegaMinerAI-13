__author__ = 'Tarnasa'

import random

from tools import *
from catscan import *


def play(game):
    toys = [toy for toy in game.droids if toy.owner != game.playerID]
    kittens = [kitten for kitten in game.droids if kitten.owner == game.playerID]

    for kitten in kittens:
        for _ in xrange(kitten.maxMovement):
            possible_moves = [[1, 0], [0, -1], [-1, 0], [0, 1]]
            possible_moves = [[kitten.x + move[0], kitten.y + move[1]] for move in possible_moves]
            possible_moves = [move for move in possible_moves if
                              inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1, move[0], move[1]) and
                              len(game.grid[move[0]][move[1]]) == 1]
            if possible_moves:
                x_off, y_off = random.choice(possible_moves)
                cat_move(game, kitten, kitten.x + x_off, kitten.y + y_off)

        if kitten.attack < 0:
            possible_toys = [playmate for playmate in kittens if
                             manhattan(playmate.x, playmate.y, kitten.x, kitten.y) <= kitten.range]
        else:
            possible_toys = [toy for toy in toys if manhattan(toy.x, toy.y, kitten.x, kitten.y) <= kitten.range]
        for _ in xrange(kitten.maxAttacks):
            if possible_toys:
                toy = random.choice(possible_toys)
                kitten.operate(toy.x, toy.y)