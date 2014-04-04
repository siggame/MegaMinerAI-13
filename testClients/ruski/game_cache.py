class game_cache:

  def __init__(self, ai):
    self.ai = ai

    self.my_spawning = dict()
    self.enemy_spawning = dict()

    self.my_hangars = dict()
    self.enemy_hangars = dict()

    self.walls = dict()

    self.my_droids = dict()
    self.enemy_droids = dict()

  def update_all(self):
    self.update_tiles()
    self.update_droids()

  def update_droids(self):
    self.my_hangars = dict()
    self.enemy_hangars = dict()

    self.walls = dict()

    self.my_droids = dict()
    self.enemy_droids = dict()


    for droid in self.ai.droids:
      if droid.variant == 5: #WALL
        self.walls[(droid.x, droid.y)] = droid

      elif droid.variant == 7: #HANGAR
        if droid.owner == self.ai.playerID:
          self.my_hangars[(droid.x, droid.y)] = droid
        elif droid.owner == self.ai.playerID^1:
          self.enemy_hangars[(droid.x, droid.y)] = droid

      else: #DROID
        if droid.owner == self.ai.playerID:
          self.my_droids[(droid.x, droid.y)] = droid
        elif droid.owner == self.ai.playerID^1:
          self.enemy_droids[(droid.x, droid.y)] = droid

    return True


  def update_tiles(self):
    self.my_spawning = dict()
    self.enemy_spawning = dict()

    for tile in self.ai.tiles:
      if tile.turnsUntilAssembled > 0: #ASSEMBLING TILE
        if tile.owner == self.ai.playerID:
          self.my_spawning[(tile.x, tile.y)] = tile
        elif tile.owner == self.ai.playerID^1:
          self.enemy_droids[(tile.x, tile.y)] = tile
    return True




