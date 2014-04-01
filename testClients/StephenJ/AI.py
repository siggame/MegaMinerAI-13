#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
from seastar import Seastar
from vexulizer.megaminer13 import DroidsVexulizer
        
TILE_WALL = 0
TILE_TURRET = 1
TILE_BASE = 2

UNIT_CLAW = 0
UNIT_ARCHER = 1 
UNIT_ENGINEER = 2
UNIT_HACKER = 3
UNIT_TURRET = 4 # This is a unit type?
UNIT_TERMINATOR = 5 

NEUTRAL_PLAYER = 2

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "ActionBot"

  @staticmethod
  def password():
    return "HamSandwich"

  ##This function is called once, before your first turn
  def init(self):
    self.sea = Seastar(self.getMapWidth(),self.getMapHeight())
    self.vex = DroidsVexulizer(self)
    self.building = set()
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  def validate(self):
    #With rigor, check properties
    for droid in self.droids:
        assert droid.getHealthLeft() <= droid.getMaxHealth()
        assert droid.getMovementLeft() <= droid.getMaxMovement()
        assert droid.getArmor() <= droid.getMaxArmor()
        assert droid.getAttacksLeft() <= droid.GetAttacks()
        
    for tile in self.tiles:
        assert tile.getScrapAmount() > 0
        assert tile.getTurnsUntilAssembled() >= 0
        assert (tile.getOwner() == NEUTRAL_PLAYER and tile.getTurnsUntilAssembled() == 0) or tile.owner != NEUTRAL_PLAYER

  def distance(self, c1, c2):
    return abs(c1[0]-c2[0])+abs(c1[1]-c2[1])

  def attack_set(self, unit, targets):
    starting_attacks = unit.getAttacksLeft()
    if len(targets) > 0 and unit.GetAttacksLeft() > 0:
        targets = filter(lambda x: x.getHealthLeft() > 0 and self.distance( (x.getX(),x.getY()), (unit.getX(), unit.getY()) ) < unit.getRange(), self.targets) 
        if len(targets) > 0:
            closest = min(targets, key=lambda x: self.distance( (x.getX(),x.getY()), (unit.getX(), unit.getY()) ) )
            unit.operate(closest) 
            assert unit.getAttacksLeft() < starting_attacks
            return True
    return False

  def follow_path(self, unit, path, fight=True):
    if len(path) > 1: # Assuming you can't move onto your target
        for step in path:
            if unit.GetMovementLeft() == 0:
                break
            if self.distance(step,(unit.getX(),unit.getY())) != 1:
                break
            unit.move(step[0],step[1])
            self.attack_set(unit, self.enemycontrol + self.enemybases)
    while self.attack_set(unit, self.enemycontrol + self.enemybases):
        pass

  def update_state(self):
    # Player objects
    self.me = [ x for x in self.players if x.getId() == self.getPlayerID() ][0]
    self.myid = self.getPlayerID()
    self.enemy = [ x for x in self.players if x.getId() != self.getPlayerID()][0]
    self.enemyid = enemy.getId()
    assert myid != enemyid
    
    # My Droids
    self.mydroids = [ x for x in self.droids if x.getOwner() == self.myid
        and x.getCurrentHealth() > 0 ]

    gf = lambda x: x.getHackedTurnsLeft() == 0
    hf = lambda x: x.getHackedTurnsLeft() > 0

    # Droids filter on hacked ness
    self.mydroids_g = filter(gf, self.mydroids)
    self.mydroids_h = filter(hf, self.mydroids)
   
    # Enemy Droids
    self.enemydroids = set([ x for x in self.droids if x.getOwner() == self.enemyid
        and x.getCurrentHealth() > 0])

    # Droids filter on hacked ness
    self.enemydroids_g = filter(gf, self.enemydroids)
    self.enemydroids_h = filter(hf, self.enemydroids)

    self.mycontrol = self.mydroids_g + self.enemydroids_h
    self.enemycontrol = self.mydroids_h + self.enemydroids_g    

    # Tiles
    self.mytiles = [ x for x in self.tiles if x.getOwner() == myid ]
    self.enemytiles = [ x for x in self.tiles if x.getOwner() == enemyid ]

    #Base tiles
    wf = lambda x: x.getTypeToAssemble() == 2
    self.mybases = filter(wf,self.mytiles)
    self.enemybases = filter(wf,self.enemybases)

    #Built walls
    wf = lambda x: x.getTurnsUntilAssembled() == 0 and x.getTypeToAssemble() == TILE_WALL and x.getHealth() > 0
    self.mywalls = filter(wf, self.mytiles)
    self.enemywalls = filter(wf, self.enemytiles)

    #Built Turrets
    wf = lambda x: x.getTurnsUntilAssembled() == 0 and x.getTypeToAssemble() == TILE_TURRET and x.getHealth() > 0
    self.myturrets = filter(wf, self.mytiles)
    self.enemyturrets = filter(wf, self.enemytiles)

    #Building wall tile
    wf = lambda x: x.getTurnsUntilAssembled() > 0 and x.getTypeToAssemble() == TILE_WALL
    self.mywalls_b = filter(wf, self.mytiles)
    self.enemywalls_b = filter(wf, self.enemytiles)
    #Building (next turn)
    wf = lambda x: x.getTurnsUntilAssembled() == 1 and x.getTypeToAssemble() == TILE_WALL
    self.mywalls_n = filter(wf, self.mytiles)
    self.enemywalls_n = filter(wf, self.enemytiles)
   
    #Building turret tile
    wf = lambda x: x.getTurnsUntilAssembled() > 0 and x.getTypeToAssemble() == TILE_TURRET
    self.myturrets_b = filter(wf, self.mytiles)
    self.enemyturrets_b = filter(wf, self.enemytiles)
    #Building (next turn)
    wf = lambda x: x.getTurnsUntilAssembled() == 1 and x.getTypeToAssemble() == TILE_TURRET
    self.myturrets_n = filter(wf, self.mytiles)
    self.enemyturrests_n = filter(wf, self.enemytiles) 

    # Neutral tiles
    self.neutraltiles = [ x for x in self.tiles if x.getOwner() == 2]
    wf = lambda x: x.getTurnsUntilAssembled() == 0 and x.getTypeToAssemble() == TILE_WALL and x.getHealth() > 0
    self.neutralwalls = filter(wf, self.neutraltiles)
    wf = lambda x: x.getTurnsUntilAssembled() == 0 and x.getTypeToAssemble() == TILE_TURRET and x.getHealth() > 0
    self.neutralturrets = filter(wf, self.neutraltiles)
    assert len(self.neutralturrets) == 0 

    # Dicts, (x,y) -> tiles and units
    self.tilesxy = {}
    for tile in self.tiles:
        self.tilesxy[(tile.getX(),tile.getY())] = tile
    self.unitsxy = {}
    for unit in self.droids:
        self.unitsxy[(unit.getX(),unit.getY())] = unit
     
    # Seastar layers
    LAYER_MY_CONTROL = 1
    LAYER_ENEMY_CONTROL = 2
    LAYER_NEUTRAL_WALLS = 4
    LAYER_ENEMY_WALLS = 8
    LAYER_MY_WALLS = 16
    LAYER_NEXT_WALLS = 32
    LAYER_NEUTRAL_TURRETS = 64
    LAYER_ENEMY_TURRETS = 128
    LAYER_MY_TURRETS = 256
    LAYER_NEXT_TURRETS = 512
    LAYER_ENEMY_BASES = 1024
    LAYER_MY_BASES = 2048
    LAYER_BUILDING_UNITS = 4096

    # Bitwise or to combine layers into a mask
    BLOCKING = LAYER_ENEMY_CONTROL | LAYER_NEUTRAL_WALLS | \
        LAYER_ENEMY_WALLS | LAYER_MY_WALLS | LAYER_NEXT_WALLS | LAYER_NEUTRAL_TURRETS | \
        LAYER_ENEMY_TURRETS | LAYER_MY_TURRETS | LAYER_NEXT_TURRETS | \
        LAYER_ENEMY_BASES | LAYER_BUILDING_UNITS 
    self.sea.set_blocking(BLOCKING)
    self.sea.reset_obstacles()
    
    # Seastar: Add layers
    self.sea.add_mappables(self.mycontrol, LAYER_MY_DROIDS)
    self.sea.add_mappables(self.enemycontrol, LAYER_ENEMY_DROIDS)    
    self.sea.add_mappables(self.neutralwalls, LAYER_NEUTRAL_WALLS)    
    self.sea.add_mappables(self.enemywalls, LAYER_ENEMY_WALLS)    
    self.sea.add_mappables(self.mywalls, LAYER_MY_WALLS)    
    self.sea.add_mappables(self.mywalls_n+self.enemywalls_n, LAYER_NEXT_WALLS)    
    self.sea.add_mappables(self.neutralturrets, LAYER_NEUTRAL_TURRETS)    
    self.sea.add_mappables(self.enemyturrets, LAYER_ENEMY_TURRETS)    
    self.sea.add_mappables(self.myturrets, LAYER_MY_TURRETS)    
    self.sea.add_mappables(self.myturrets_n+self.my_enemyturrets_n, LAYER_NEXT_TURRETS)    
    self.sea.add_mappables(self.enemybases, LAYER_ENEMY_BASES)    
    self.sea.add_mappables(self.mybases, LAYER_MY_BASES)
    self.sea.add_obstacles(self.building, LAYER_BUILDING_UNITS)   

    #Push the game state into the vexulizer.
    self.vex.snapshot(self)
    

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    update_state()

    # Tiles don't seem to have a maxHealth property (??)
    # Verify tiles don't have negative health at the start of a turn
    for tile in self.tiles:
        assert tiles.getHealth() >= 0

    # Mappables
    assert len(self.mappables) > 0 # This was a problem in reef

    # Before we start, check some stuff out, then continue.
    validate()    

    if True:
        initial_scrap = self.me.getScrapAmount()
        # Validate that you can only spawn units on the base tiles:
        for tile in neutraltiles:
            tile.assemble(self.modelVariants[0].getId())
            assert initial_scrap == self.me.getScrapAmount()
        
    if True:
        # Validate you can't orbital drop onto a tile you already own.
        initial_scrap = self.me.getScrapAmount()
        for tile in mytiles:
            tile.orbitalDrop(tile.getX(), tile.getY(), TILE_WALL)
            assert initial_scrap == self.me.getScrapAmount()
            tile.orbitalDrop(tile.getX(), tile.getY(), TILE_TURRET)
            assert initial_scrap == self.me.getScrapAmount()
  
    self.building = set()
    while self.me.getScrapAmount() >= min([ variant.getCost() for variant in self.modelVariants ]):
        initial_scrap = self.me.getScrapAmount()
        #Simple AI, pick a unit type, (Other than turret, and drop those)
        for variant in self.modelVariants:
            if variant.getVariant() == UNIT_TURRET:
                continue
            if variant.getCost() > self.me.getScrapAmount():
                continue
            for tile in self.mybases:
                if (tile.getX(), tile.getY()) in self.unitsxy:
                    continue
                if (tile.getX(), tile.getY()) in self.building:
                    continue
                #If we've made it this far, we can spawn the variant
                tile.assemble(variant.getVariant())
                self.building.add( (tile.getX(), tile.getY()) )
                assert initial_scrap > self.me.getScrapAmount()
                break

    update_state()

    #Have all your units go after the enemy base
    tomove = {}
    for unit in self.mycontrol:
        tomove[unit.getId()] = unit

    while len(tomove) > 0:
        starts = [ (unit.getX(), unit.getY()) for (_,unit) in tomove.iteritems() ]
        ends = [ (unit.getX(), unit.getY()) for unit in self.enemycontrol + self.enemybases ]
        p = self.sea.get_path(starts,ends)
        if len(p) > 0:
            self.follow_path(unit,path)
        tomove.pop(unit.getId(),None)
        update_state()
         
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
