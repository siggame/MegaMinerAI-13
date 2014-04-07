__author__ = 'Tarnasa'

import itertools  # Contains heapq as well?
from tools import *


def setup_cat_scan(game):
    for breed in game.modelVariants:
        breed.count_enemy = 0
        breed.count_my = 0


def cat_scan(game):
    game.grid = [[[] for _ in xrange(game.mapHeight)] for _ in xrange(game.mapWidth)]
    for tile in game.tiles:
        game.grid[tile.x][tile.y].append(tile)
        tile.closed = False
        tile.open = False
    for droid in game.droids:
        game.grid[droid.x][droid.y].append(droid)
        droid.possible_damage = []  # Heap
        # scan shields
        scan_shields(game, droid)

    game.toys = [toy for toy in game.droids if toy.owner != (game.playerID ^ toy.hackedTurnsLeft > 0)]
    game.kittens = [kitten for kitten in game.droids if kitten.owner == (game.playerID ^ kitten.hackedTurnsLeft > 0)]

    scan_possible_damage(game)

    analyze_strategy(game)


def cat_move(game, droid, x, y):
    if droid in game.grid[droid.x][droid.y]:
        game.grid[droid.x][droid.y].remove(droid)
    success = droid.move(x, y)
    if success:
        game.grid[x][y].append(droid)
    return success


def scan_shields(game, droid):
    droid.shields = []
    for x_off, y_off in [[1, 0], [0, -1], [-1, 0], [0, 1]]:
        test_x, test_y = x_off + droid.x, y_off + droid.y  # Woah now, careful with those tuples
        if inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1, test_x, test_y) and len(game.grid[test_x][test_y]) == 2:
            shield = game.grid[droid.x + x_off][droid.y + y_off][1]
            if (shield.owner ^ shield.hackedTurnsLeft > 0) == (droid.owner ^ droid.hackedTurnsLeft > 0):
                droid.shields.append(shield)


def scan_possible_damage(game):
    # Simulate all possible attacks
    for droid_a, droid_b in itertools.combinations(game.droids, 2):
        if (droid_a.owner ^ droid_a.hackedTurnsLeft > 0) != (droid_b.owner ^ droid_b.hackedTurnsLeft > 0):
            dis = manhattan(droid_a.x, droid_a.y, droid_b.x, droid_b.y)
            if dis <= droid_a.range + droid_a.maxMovement:
                heapq.heappush(droid_b.possible_damage, (-droid_a.attack, droid_b.maxAttacks))  # TODO Incorrect sorting
            if dis <= droid_b.range + droid_b.maxMovement:
                heapq.heappush(droid_a.possible_damage, (-droid_b.attack, droid_a.maxAttacks))
    # Simulate best attacks
    for droid in game.droids:
        top_damage = []
        possible_attacks = 4  # Account for blocking with allied droids
        for x_off, y_off in [[1, 0], [0, -1], [-1, 0], [0, 1]]:
            if len(game.grid[droid.x + x_off][droid.y + y_off]) == 2:
                shield = game.grid[droid.x + x_off][droid.y + y_off][1]
                if (shield.owner ^ shield.hackedTurnsLeft > 0) == (droid.owner ^ droid.hackedTurnsLeft > 0):
                    possible_attacks -= 1
        if possible_attacks > len(droid.possible_damage):
            possible_attacks = len(droid.possible_damage)
        for _ in xrange(possible_attacks):
            damage, multiplier = heapq.heappop(droid.possible_damage)
            for _ in xrange(multiplier):
                top_damage.append(-damage)
        droid.possible_armor = droid.armor
        droid.possible_health = droid.healthLeft
        # Simulate actual attacks
        for damage in reversed(top_damage):
            real_damage = damage
            if droid.possible_armor > 0:
                real_damage = int(damage * ((droid.maxArmor - droid.possible_armor) / float(droid.maxArmor)))
                droid.possible_armor -= damage
                if droid.possible_armor < 0:
                    droid.possible_armor = 0
            droid.possible_health -= real_damage


def analyze_strategy(game):
    pass