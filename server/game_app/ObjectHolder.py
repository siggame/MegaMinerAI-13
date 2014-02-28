import objects

class ObjectHolder(dict):
  def __init__(self, *args, **kwargs):
    dict.__init__(self, *args, **kwargs)
    self.players = []
    self.mappables = []
    self.droids = []
    self.tiles = []
    self.modelVariants = []

  def __setitem__(self, key, value):
    if key in self:
      self.__delitem__(key)
    dict.__setitem__(self, key, value)
    if isinstance(value, objects.Player):
      self.players.append(value)
    if isinstance(value, objects.Mappable):
      self.mappables.append(value)
    if isinstance(value, objects.Droid):
      self.droids.append(value)
    if isinstance(value, objects.Tile):
      self.tiles.append(value)
    if isinstance(value, objects.ModelVariant):
      self.modelVariants.append(value)

  def __delitem__(self, key):
    value = self[key]
    dict.__delitem__(self, key)
    if value in self.players:
      self.players.remove(value)
    if value in self.mappables:
      self.mappables.remove(value)
    if value in self.droids:
      self.droids.remove(value)
    if value in self.tiles:
      self.tiles.remove(value)
    if value in self.modelVariants:
      self.modelVariants.remove(value)

  def clear(self):
    for i in self.keys():
      del self[i]
