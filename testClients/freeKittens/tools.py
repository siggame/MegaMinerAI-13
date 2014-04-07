__author__ = 'Tarnasa'

import heapq


def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def inrange(x1, x2, x):
    return x1 <= x <= x2


def inbox(x1, y1, x2, y2, x, y):
    return inrange(x1, x2, x) and inrange(y1, y2, y)


def can_move_to(game, droid, target):
    if manhattan(droid.x, droid.y, target.x, target.y) > droid.movementLeft:
        return False
    return True


def a_star_max(game, x1, y1, x2, y2, max_cost):
    neighbor_offsets = [[1, 0], [0, -1], [-1, 0], [0, 1]]

    open_heap = []   # Heap

    heapq.heappush(open_heap, game.grid[x1][y1][0])
    game.grid[x1][y1][0].open = True

    game.grid[x1][y1][0].g_score = 0
    game.grid[x1][y1][0].f_score = manhattan(x1, y1, x2, y2)

    while open_heap:
        top = heapq.heappop(open_heap)
        top.open = False
        if top.x == x2 and top.y == y2:
            path = [top]
            tile = top
            while tile.x != x1 or tile.y != y1:
                tile = top.came_from
                path.append(tile)
            return reversed(path)

        top.closed = True
        for x_off, y_off in neighbor_offsets:
            neighbor_x = top.x + x_off
            neighbor_y = top.y + y_off
            if inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1, neighbor_x, neighbor_y) and\
                    len(game.grid[neighbor_x][neighbor_y]) == 1 and not game.grid[neighbor_x][neighbor_y][0].closed:
                tentative_g_score = top.g_score + 1
                neighbor = game.grid[neighbor_x][neighbor_y][0]
                if tentative_g_score <= max_cost and (not neighbor.open or tentative_g_score < neighbor.g_score):
                    neighbor.came_from = top
                    neighbor.g_score = tentative_g_score
                    neighbor.f_score = tentative_g_score + manhattan(neighbor_x, neighbor_y, x2, y2)
                    if not neighbor.open:
                        neighbor.open = True
                        heapq.heappush(open_heap, neighbor)


def a_star(game, x1, y1, x2, y2):
    neighbor_offsets = [[1, 0], [0, -1], [-1, 0], [0, 1]]

    open_heap = []   # Heap

    heapq.heappush(open_heap, game.grid[x1][y1][0])
    game.grid[x1][y1][0].open = True

    game.grid[x1][y1][0].g_score = 0
    game.grid[x1][y1][0].f_score = manhattan(x1, y1, x2, y2)

    while open_heap:
        top = heapq.heappop(open_heap)
        top.open = False
        if top.x == x2 and top.y == y2:
            path = [top]
            tile = top
            while tile.x != x1 or tile.y != y1:
                tile = top.came_from
                path.append(tile)
            return reversed(path)

        top.closed = True
        for x_off, y_off in neighbor_offsets:
            neighbor_x = top.x + x_off
            neighbor_y = top.y + y_off
            if inbox(0, 0, game.mapWidth - 1, game.mapHeight - 1, neighbor_x, neighbor_y) and\
                    len(game.grid[neighbor_x][neighbor_y]) == 1 and not game.grid[neighbor_x][neighbor_y][0].closed:
                tentative_g_score = top.g_score + 1
                neighbor = game.grid[neighbor_x][neighbor_y][0]
                if not neighbor.open or tentative_g_score < neighbor.g_score:
                    neighbor.came_from = top
                    neighbor.g_score = tentative_g_score
                    neighbor.f_score = tentative_g_score + manhattan(neighbor_x, neighbor_y, x2, y2)
                    if not neighbor.open:
                        neighbor.open = True
                        heapq.heappush(open_heap, neighbor)

    return []


def move_to():
    pass