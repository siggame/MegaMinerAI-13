from curses import COLOR_BLACK, COLOR_BLUE, COLOR_CYAN, COLOR_GREEN 
from curses import COLOR_MAGENTA, COLOR_RED, COLOR_WHITE, COLOR_YELLOW

import curses

#: Color definitions, Key: Color Name -> ( Foreground, Background )
#: You can try to use an (r,g,b) (1-1000)  tuple but it might now work gewd.
COLOR_DEFINITIONS = {
    # Required:
    "CURSOR_COLOR" : (COLOR_YELLOW, COLOR_BLACK),
    "ENEMY_COLOR"  : (COLOR_RED, COLOR_BLACK),
    "ENEMY_COLOR_HACKED": (COLOR_MAGENTA, COLOR_BLACK),
    "MY_COLOR"     : (COLOR_GREEN, COLOR_BLACK),
    "MY_COLOR_HACKED": (COLOR_CYAN, COLOR_BLACK), 
    "WALL_COLOR"   : (COLOR_WHITE, COLOR_WHITE),
}

class ScreenColors(object):
    """
    An object to allocate and look up colors in a convient naming scheme.
    """    
    def __init__(self):
        c = 2 
        #: The next available color to allocate for user defined colors
        self.colorcounter = 9
        #: The colors that have been allocated by the user so far
        self.allocated = {} 
        #: A map from the name to the color identifier. 
        self.nametoid = {}
        curses.start_color()
        for (k,v) in COLOR_DEFINITIONS.iteritems():
            fg = self.init_color(v[0])
            bg = self.init_color(v[1])
            self.nametoid[k] = c
            curses.init_pair(c,fg,bg)
            c += 1

    def init_color(self,t):
        """
        Attempts to allocate a custom color. If the color you try to allocate
        has already been allocated once, it will return the old color
        
        If the value passed is not a 3-tuple, this function will return the
        input parameter.       
        """
        try:
            return self.allocated[t]
        except KeyError:
            pass
        try:
            if len(t) == 3:
                if self.colorcounter > curses.COLORS:
                    return 1
                if not curses.can_change_color():
                    return 1
                curses.init_color(self.colorcounter,t[0],t[1],t[2])
                c = self.colorcounter
                self.allocated[t] = c
                self.colorcounter += 1
                return c
            else:
                return t
        except (KeyError, IndexError, TypeError) as e:
            return t
    
    def get_color(self, k):
        """
        Returns the number for the curses color pair represented by the name k
        """
        x = curses.color_pair(self.nametoid[k])
        return x
