__author__ = 'Tarnasa'

import random

from cat_scan import *


def play(game):
    for kitten in game.kittens:
        move_x = random.randint(0, kitten.movementLeft)
        move_y = random.randint(0, kitten.movementLeft - move_x)
        move_x *= random.choice([-1, 1])
        move_y *= random.choice([-1, 1])
        move_to(game, kitten, kitten.x + move_x, kitten.y + move_y)

        if kitten.attack < 0:
            possible_toys = [playmate for playmate in game.kittens if
                             tools.manhattan(playmate.x, playmate.y, kitten.x, kitten.y) <= kitten.range]
        else:
            possible_toys = [toy for toy in game.toys if
                             tools.manhattan(toy.x, toy.y, kitten.x, kitten.y) <= kitten.range]
        for _ in xrange(kitten.maxAttacks):
            if possible_toys:
                toy = random.choice(possible_toys)
                kitten.operate(toy.x, toy.y)


def play_fast(game):
    available_kittens = list(game.kittens_by_range)
    for best_toy in game.toys_by_health:
        for attacker in available_kittens:
            # Calculate best position
            best_dis = 0
            best_position = None
            for x in range(best_toy.x - attacker.range, best_toy.y + attacker.range + 1):
                d = attacker.range - abs(x - best_toy.x)
                for y in range(best_toy.y - d, best_toy.y + d + 1):
                    distance = tools.manhattan(attacker.x, attacker.y, x, y)
                    if tools.inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1, x, y) and\
                            len(game.grid[x][y]) == 1 and\
                            distance <= attacker.movementLeft:
                        if distance > best_dis:
                            best_dis = distance
                            best_position = game.grid[x][y][0]
                            if distance == attacker.movementLeft:
                                break
                else:  # KITTEN MAGIC
                    continue
                break
            if best_position:
                move_to(game, attacker, best_position.x, best_position.y)
                if tools.manhattan(attacker.x, attacker.y, best_toy.x, best_toy.y) <= attacker.range:
                    while attacker.attacksLeft and best_toy.healthLeft > 0:
                        if not attacker.operate(best_toy.x, best_toy.y):
                            break
                    if best_toy.healthLeft <= 0:
                        break
        available_kittens[:] = [kitten for kitten in available_kittens if kitten.attacksLeft > 0 and kitten.attack > 0]
    interesting_toys = [toy for toy in game.toys if toy.healthLeft > 0]
    available_kittens = [kitten for kitten in game.kittens if kitten.movementLeft > 0]
    for kitten in available_kittens:
        toy = random.choice(interesting_toys)
        move_towards(game, kitten, toy.x, toy.y)