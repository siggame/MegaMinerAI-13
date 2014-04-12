__author__ = 'Tarnasa'

import heapq


def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def inrange(x1, x2, x):
    return x1 <= x <= x2


def inbox(x1, y1, x2, y2, x, y):
    return inrange(x1, x2, x) and inrange(y1, y2, y)


def get_cells_in_range(game, x_center, y_center, r):
    cells = []
    for x in range(x_center - r, x_center + r + 1):
        dis = r - abs(x - x_center)
        for y in range(y_center - dis, y_center + dis + 1):
            if inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1, x, y):
                cells.append(game.grid[x][y])
    return cells


def get_empty_cells_in_range(game, x_center, y_center, r):
    cells = []
    for x in range(x_center - r, x_center + r + 1):
        dis = r - abs(x - x_center)
        for y in range(y_center - dis, y_center + dis + 1):
            if inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1, x, y) and len(game.grid[x][y]) == 1:
                cells.append(game.grid[x][y])
    return cells


def optimal_attack_position(game, attacker, target):
    best_dis = 0
    best_position = None
    for x in range(target.x - attacker.range, target.y + attacker.range + 1):
        d = attacker.range - abs(x - target.x)
        for y in range(target.y - d, target.y + d + 1):
            distance = manhattan(attacker.x, attacker.y, x, y)
            if inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1, x, y) and\
                    len(game.grid[x][y]) == 1 and\
                    distance <= attacker.movementLeft:
                if distance > best_dis:
                    best_dis = distance
                    best_position = game.grid[x][y][0]
                    if distance == attacker.movementLeft:
                        return best_position
    return best_position


def a_star_max(game, x1, y1, x2, y2, max_cost):
    if (x1 == x2 and y1 == y2) or max_cost == 0:
        return []

    neighbor_offsets = [[1, 0], [0, -1], [-1, 0], [0, 1]]

    open_set = set()
    open_heap = []   # Heap
    closed_set = set()

    heapq.heappush(open_heap, (0, game.grid[x1][y1][0]))
    open_set.add(game.grid[x1][y1][0])

    game.grid[x1][y1][0].g_score = 0
    game.grid[x1][y1][0].f_score = manhattan(x1, y1, x2, y2)

    while open_heap:
        _, top = heapq.heappop(open_heap)
        if top.x == x2 and top.y == y2:
            path = []
            while top.x != x1 or top.y != y1:
                path.append(top)
                top = top.came_from
            return reversed(path)

        open_set.remove(top)
        closed_set.add(top)
        for x_off, y_off in neighbor_offsets:
            neighbor_x = top.x + x_off
            neighbor_y = top.y + y_off
            if inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1, neighbor_x, neighbor_y) and\
                    len(game.grid[neighbor_x][neighbor_y]) == 1 and\
                    game.grid[neighbor_x][neighbor_y][0] not in closed_set:
                tentative_g_score = top.g_score + 1
                neighbor = game.grid[neighbor_x][neighbor_y][0]
                if tentative_g_score <= max_cost and (neighbor not in open_set or tentative_g_score < neighbor.g_score):
                    neighbor.came_from = top
                    neighbor.g_score = tentative_g_score
                    neighbor.f_score = tentative_g_score + manhattan(neighbor_x, neighbor_y, x2, y2)
                    if neighbor not in open_set:
                        open_set.add(neighbor)
                        heapq.heappush(open_heap, (neighbor.f_score, neighbor))
    return []


def a_star(game, x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return []

    neighbor_offsets = [[1, 0], [0, -1], [-1, 0], [0, 1]]

    open_set = set()
    open_heap = []   # Heap
    closed_set = set()

    heapq.heappush(open_heap, (0, game.grid[x1][y1][0]))
    open_set.add(game.grid[x1][y1][0])

    game.grid[x1][y1][0].g_score = 0
    game.grid[x1][y1][0].f_score = manhattan(x1, y1, x2, y2)

    while open_heap:
        _, top = heapq.heappop(open_heap)
        if top.x == x2 and top.y == y2:
            path = []
            while top.x != x1 or top.y != y1:
                path.append(top)
                top = top.came_from
            return reversed(path)

        open_set.remove(top)
        closed_set.add(top)
        for x_off, y_off in neighbor_offsets:
            neighbor_x = top.x + x_off
            neighbor_y = top.y + y_off
            if inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1, neighbor_x, neighbor_y) and\
                    len(game.grid[neighbor_x][neighbor_y]) == 1 and\
                    game.grid[neighbor_x][neighbor_y][0] not in closed_set:
                tentative_g_score = top.g_score + 1
                neighbor = game.grid[neighbor_x][neighbor_y][0]
                if neighbor not in open_set or tentative_g_score < neighbor.g_score:
                    neighbor.came_from = top
                    neighbor.g_score = tentative_g_score
                    neighbor.f_score = tentative_g_score + manhattan(neighbor_x, neighbor_y, x2, y2)
                    if neighbor not in open_set:
                        open_set.add(neighbor)
                        heapq.heappush(open_heap, (neighbor.f_score, neighbor))
    return []


def a_star_ignore_end(game, x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return []

    neighbor_offsets = [[1, 0], [0, -1], [-1, 0], [0, 1]]

    open_set = set()
    open_heap = []   # Heap
    closed_set = set()

    heapq.heappush(open_heap, (0, game.grid[x1][y1][0]))
    open_set.add(game.grid[x1][y1][0])

    game.grid[x1][y1][0].g_score = 0
    game.grid[x1][y1][0].f_score = manhattan(x1, y1, x2, y2)

    while open_heap:
        _, top = heapq.heappop(open_heap)
        if top.x == x2 and top.y == y2:
            path = []
            while top.x != x1 or top.y != y1:
                path.append(top)
                top = top.came_from
            return reversed(path)

        open_set.remove(top)
        closed_set.add(top)
        for x_off, y_off in neighbor_offsets:
            neighbor_x = top.x + x_off
            neighbor_y = top.y + y_off
            if (neighbor_x == x2 and neighbor_y == y2) or\
                    (inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1, neighbor_x, neighbor_y) and\
                    len(game.grid[neighbor_x][neighbor_y]) == 1 and\
                    game.grid[neighbor_x][neighbor_y][0] not in closed_set):
                tentative_g_score = top.g_score + 1
                neighbor = game.grid[neighbor_x][neighbor_y][0]
                if neighbor not in open_set or tentative_g_score < neighbor.g_score:
                    neighbor.came_from = top
                    neighbor.g_score = tentative_g_score
                    neighbor.f_score = tentative_g_score + manhattan(neighbor_x, neighbor_y, x2, y2)
                    if neighbor not in open_set:
                        open_set.add(neighbor)
                        heapq.heappush(open_heap, (neighbor.f_score, neighbor))
    return []