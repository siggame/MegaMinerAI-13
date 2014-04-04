class GameHistory:
  def __init__(ai):
    self._ai = ai
    self.history = []
    pass

  def saveSnapshot():
    snapshot = [[[] for _ in self._ai.mapHeight] for _ in self._ai.mapWidth]

    for tile in self_ai.tiles:
      if tile.owner == 0:
        snapshot[tile.x][tile.y].append('0')
      elif tile.owner == 1:
        snapshot[tile.x][tile.y].append('1')
      elif tile.owner == 3:
        snapshot[tile.x][tile.y].append('W')

