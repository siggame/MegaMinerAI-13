__author__ = 'Tarnasa'

import tools

import heapq


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
        # Scan shields
        #scan_shields(game, droid)

    game.toys = [toy for toy in game.droids if toy.owner != (game.playerID ^ toy.hackedTurnsLeft > 0)]
    game.kittens = [kitten for kitten in game.droids if kitten.owner == (game.playerID ^ kitten.hackedTurnsLeft > 0)]

    game.toys_by_health = list(game.toys)
    game.toys_by_health.sort(key=lambda t: t.healthLeft)

    game.kittens_by_range = list(game.kittens)
    game.kittens_by_range.sort(key=lambda t: t.range)

    #scan_possible_damage(game) # TOO SLOW

    analyze_strategy(game)


def cat_move(game, droid, x, y):
    if droid in game.grid[droid.x][droid.y]:
        game.grid[droid.x][droid.y].remove(droid)
    success = droid.move(x, y)
    if success:
        game.grid[x][y].append(droid)
    return success


def move_to(game, droid, x, y):
    path = tools.a_star_max(game, droid.x, droid.y, x, y, droid.movementLeft)
    for step in path:
        if not cat_move(game, droid, step.x, step.y):
            print('Error moving to {} {}\n'.format(x, y))
            return False
    return True


def move_towards(game, droid, x, y):
    path = tools.a_star_ignore_end(game, droid.x, droid.y, x, y)
    for step in path:
        if droid.movementLeft > 0:
            if not cat_move(game, droid, step.x, step.y):
                return False
        else:
            break
    return True


def scan_shields(game, droid):
    droid.shields = []
    for x_off, y_off in [[1, 0], [0, -1], [-1, 0], [0, 1]]:
        test_x, test_y = x_off + droid.x, y_off + droid.y  # Woah now, careful with those tuples
        if tools.inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1, test_x, test_y) and\
                len(game.grid[test_x][test_y]) == 2:
            shield = game.grid[droid.x + x_off][droid.y + y_off][1]
            if (shield.owner ^ shield.hackedTurnsLeft > 0) == (droid.owner ^ droid.hackedTurnsLeft > 0):
                droid.shields.append(shield)


def scan_possible_damage(game):
    # Simulate all possible attacks
    for kitten in game.kittens:
        for toy in game.toys:
            dis = tools.manhattan(kitten.x, kitten.y, toy.x, toy.y)
            if dis <= kitten.range + kitten.maxMovement and kitten.attack > 0:
                heapq.heappush(toy.possible_damage,
                               (kitten.attack * -toy.maxAttacks, toy))
            if dis <= toy.range + toy.maxMovement and toy.attack > 0:
                heapq.heappush(kitten.possible_damage,
                               (toy.attack * -kitten.maxAttacks, kitten))
    # Simulate possible attacks
    for droid in game.droids:
        damages = []
        melee_attacks = 4
        possible_damage = list(droid.possible_damage)
        while possible_damage:
            _, attacker = heapq.heappop(possible_damage)
            if attacker.range == 1 and melee_attacks:
                melee_attacks -= 1
            elif attacker.range > 1:
                for _ in xrange(attacker.maxAttacks):
                    damages.append(attacker.attack)
        droid.possible_armor = droid.armor
        droid.possible_health = droid.healthLeft
        # Simulate actual attacks
        for damage in reversed(damages):
            real_damage = damage
            if droid.possible_armor > 0:
                real_damage = int(damage * ((droid.maxArmor - droid.possible_armor) / float(droid.maxArmor)))
                droid.possible_armor -= damage
                if droid.possible_armor < 0:
                    droid.possible_armor = 0
            droid.possible_health -= real_damage


def analyze_strategy(game):
    pass