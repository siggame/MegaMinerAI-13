from vexulizer import Vexulizer

class DroidsVexulizer(object):
    """
    This is the object you should use to enable the Vexulizer for REEF
    (Megaminer 13). To install, include this object by doing:

    from megaminer13 import DroidsVexulizer

    Then, in your init function in AI.py:

    self.vex = DroidsVexulizer(self)

    And in your run function, you probably want, at the very list a call to
    snapshot at the beginning and end like so:

        self.vex.snapshot(self) #To capture what your opponent did
        <!-- Your AI goes here --->
        <!-- Snip --->
        self.vex.snapshot(self) #To capture what you did.

    In addition to what is suggested, you can make calls to 
    self.vex.snapshot(self) as often as you like to update the state more 
    often. In addition, you can use self.vex.breakpoint(self) which also
    updates the visualizer state, but will also pause the visualizer for
    you to inspect.

    Because the vexulizer uses curses (and is asynchronous), it probably will
    automatically shut itself off in the arena. but, in case it doesn't you
    can turn enable off before your submit it and not have to worry!
    """
    def __init__(self,ai,enable=True):
        self.enable = enable
        if not self.enable:
            return
        #: The underlying vexulizer
        self.vex = Vexulizer(ai.getMapWidth(),ai.getMapHeight())
    def update_map(self,ai):
        if not self.enable:
            return
        # Using the AI, convert each type to a dictionary and then push the
        # whole caboodle to the visualizer
        package = []
    
        variant = {0: 'C',
                   1: 'A',
                   2: 'R',
                   3: 'H',
                   4: 'T',
                   5: 'W',
                   6: 'E',
                   7: 'H'}

        for droid in ai.droids:
            if droid.owner == ai.myid:
                if droid.getVariant() == 7:
                    color = "MY_COLOR_HANGAR" 
                elif droid.getHackedTurnsLeft() > 0:
                    color = "MY_COLOR_HACKED"
                else:
                    color = "MY_COLOR"
            else:
                if droid.getVariant() == 7:
                    color = "ENEMY_COLOR_HANGAR"
                elif droid.getHackedTurnsLeft() > 0:
                    color = "ENEMY_COLOR_HACKED"
                else:
                    color = "ENEMY_COLOR"
            if droid.getVariant() == 5:
                color = "WALL_COLOR"

            package.append({
                'x':droid.getX(),
                'y':droid.getY(),
                'id':droid.getId(),
                'owner': droid.getOwner(),
                'variant': droid.getVariant(),
                'attacksLeft': droid.getAttacksLeft(),
                'healthLeft': droid.getHealthLeft(),
                'movementLeft': droid.getMovementLeft(),
                'hackedUntil': droid.getHackedTurnsLeft(),
                'hackets': droid.getHackets(),
                'v': (variant[droid.getVariant()], color)})
        self.vex.update_units(package)

    def snapshot(self,ai):
        if not self.enable:
            return
        self.update_map(ai)
        self.vex.mark_turn(ai.getTurnNumber())
    def breakpoint(self,ai):
        if not self.enable:
            return
        self.update_map(ai)
        self.vex.breakpoint(ai.getTurnNumber())
    def end(self,ai):
        if not self.enable:
            return
        self.vex.stop_debugger()
