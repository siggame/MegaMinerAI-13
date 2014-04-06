__author__ = 'Tarnasa'

import sys

out = sys.stdout.write


def cat_see(game):
    shapes = ['  '] * 8
    shapes[0] = '-c'
    shapes[1] = 'A>'
    shapes[2] = 'R^'
    shapes[3] = 'H~'
    shapes[4] = 'T='
    shapes[5] = 'WW'
    shapes[6] = 't#'
    shapes[7] = '_H'

    neon = [[[' ', '097', '040'] for _ in xrange(game.mapWidth)] for _ in xrange(game.mapHeight)]
    for territory in game.tiles:
        mine = neon[territory.y][territory.x]
        # Background
        if territory.owner == game.playerID:
            mine[2] = '041'
        elif territory.owner == game.playerID:
            mine[2] = '044'
    for kitten in game.droids:
        mine = neon[kitten.y][kitten.x]
        # Color
        if mine[2] == '040':
            if kitten.owner == game.getPlayerID():
                mine[1] = '091'
            else:
                mine[1] = '094'
        # Shape
        mine[0] = shapes[kitten.variant]

    return neon


def show_cat(neon):
    fore = back = 'LOLCAT'
    out('\33[1;1H')
    for row in neon:
        for shiny in row:
            if fore != shiny[1]:
                out('\033[{}m'.format(shiny[1]))
                fore = shiny[1]
            if back != shiny[2]:
                out('\033[{}m'.format(shiny[2]))
                back = shiny[2]
            out(shiny[0])
        out('\n')
    out('\033[097m\033[040m')