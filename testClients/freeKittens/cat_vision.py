__author__ = 'Tarnasa'

import sys
out = sys.stdout.write

def cat_see(game):
  shapes = dict()
  shapes[0] = 'c'
  shapes[1] = 'A'
  shapes[2] = 'R'
  shapes[3] = 'H'
  shapes[4] = 'T'
  shapes[5] = 'E'

  neon = [[[' ', '097', '040']] * game.getMapWidth()] * game.getMapHeight()
  for territory in game.tiles:
    mine = neon[territory.x][territory.y]
    # Background
    if territory.owner == game.getPlayerID():
      if territory.type == 2 or territory.health > 0:
        mine[2] = '101'
      else:
        mine[2] = '041'
    elif territory.owner == game.getPlayerID():
      if territory.type == 2 or territory.health > 0:
        mine[2] = '104'
      else:
        mine[2] = '044'
    # Foreground
    if territory.health > 0:
      if territory.type == 2:
        mine[0] = ':'
      else:
        mine[0] = 'X'
  for kitten in game.droids:
    mine = neon[kitten.x + kitten.y * game.getMapWidth()]
    # Color
    if mine[2] == '040':
      if kitten.owner == game.getPlayerID():
        mine[1] = '091'
      else:
        mine[1] = '094'
    # Shape
    mine[0] = shapes[kitten.variant.variant]

  return neon

def show_cat(neon):
  fore = back = 'LOLCAT'
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


