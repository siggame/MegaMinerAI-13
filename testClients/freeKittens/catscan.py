__author__ = 'Tarnasa'


def catscan(game):
    grid = [[[] for _ in xrange(game.mapHeight)] for _ in xrange(game.mapWidth)]
    for tile in game.tiles:
        grid[tile.x][tile.y].append(tile)
    for droid in game.droids:
        grid[droid.x][droid.y].append(droid)
    return grid


def cat_move(game, droid, x, y):
    if droid in game.grid[droid.x][droid.y]:
        game.grid[droid.x][droid.y].remove(droid)
    success = droid.move(x, y)
    if success:
        game.grid[x][y].append(droid)
    return success