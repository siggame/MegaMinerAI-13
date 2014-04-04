import sys

from multiprocessing import Process, Queue, Value
import curses
from time import sleep
from datetime import datetime, timedelta
from Queue import Empty
import traceback

import vexulizer
from colors import ScreenColors 

UNIT_KEY_BLACKLIST = ['v']
MAP_CURSOR_BLINK_RATE = timedelta(milliseconds=500)

class WindowBox(object):
    """
    A simple object which stores the dimensions of a curses window, supports
    a quick check of the dims relative to a potential parent and spawning the
    target window
    """

    def __init__(self, height, width, yoffset, xoffset):
        #: The height of the window (lines)
        self.height = height
        #: The width of the window (cols)
        self.width = width
        #: The x offset for where the window should be drawn
        self.xoffset = xoffset
        #: The y offset for where the window should be drawn
        self.yoffset = yoffset
    
    def check_dims(self,parent):
        """
        Given a parent curses object (one with getmaxyx() as a method)
        determine if this WindowBox will fit inside
        """
        (ty,tx) = parent.getmaxyx()
        if self.xoffset+self.width > tx:
            return False
        if self.yoffset+self.height > ty:
            return False
        return True
 
    def create(self, parent=None):
        """
        Creates the window defined by this object as a derived window of parent
        (using xoffset and yoffset as a relative offset) or a new window if no
        parent is provided.
        """
        if parent:
            return parent.derwin(self.height,self.width,self.yoffset,self.xoffset)
        else:
            return curses.newwin(self.height,self.width,self.yoffset,self.xoffset) 

class AsyncCursesScreen(object):
    """
    The main viewport of the Vexulizer interface. Draws the curses screen and
    pulls tokens from the queue. Called by the Process initialized in the 
    Vexulizer object

    Curses transposes X and Y (Y comes first in the coordinate pair. for
    consistency, this object is the first that uses Y,X instead of X,Y.
    """

    def __init__(self,mapheight,mapwidth):
        #: If paused, tokens will not be pulled out the queue.
        self.paused = False
        #: If set to true, the curses screen will attempt to tear itself down.
        self.halting = False
        #: The height of the map area.
        self.mapheight = mapheight
        #: The width of the map area.
        self.mapwidth = mapwidth
    def start(self,q,running):
        """
        Starts the curses screen and does clean-up if something crashes the
        curses visualizer.
        """
        #: Set to false when the curses screen exits; shared globally
        self.running = running
        #: The shared queue that tokens are consumed from.
        self.queue = q
        try:
            curses.wrapper(self.handler)
        except:
            curses.endwin()
            #Restore the real stderr and stdout?
            sys.stderr = vexulizer.Vexulizer.rstderr
            sys.stdout = vexulizer.Vexulizer.rstdout
            print "Something went terribly wrong! Is your terminal wide enough?"
            print traceback.format_exc()
            sys.stdout.flush()
            self.running.value = False          
 
    def handler(self,stdscr):
        """
        Spawns the curses windows, then executes a loop that pulls tokens from
        the queue and passes them to the appropriate modules.
        """
        # First, draw the initial window.
        stdscr.border()
        stdscr.touchwin()
        stdscr.refresh()
        stdscr.nodelay(1)
        curses.use_default_colors()
        curses.curs_set(0)
        (ty,tx) = stdscr.getmaxyx()
        #MOVE TO COLORS.PY
        self.colors = ScreenColors()
       
        mapbox = WindowBox(self.mapheight+5, self.mapwidth*2+5, 0, 0)
        unitbox = WindowBox(self.mapheight+5, tx-(self.mapwidth*2+5), 0, self.mapwidth*2+5)
        debugbox = WindowBox(ty-(self.mapheight+5), tx, self.mapheight+5, 0)

        if tx < 120:
            curses.resizeterm(ty,120)

        if not mapbox.check_dims(stdscr):
            return
        
        if not unitbox.check_dims(stdscr):
            return

        if not unitbox.check_dims(stdscr):
            return
       
        #: The map window.
        self.game = MapWindow(mapbox, self.colors, self.mapwidth,self.mapheight)
        #: The unit viewer.
        self.unit = UnitWindow(unitbox)
        #: The debug (stdout/stderr) view.
        self.debug = DebugWindow(debugbox)
       
        #: All the pickle points we've captured so far
        self.pickles = []
        #: The turn counter
        self.tc = 0
        #: The pickle counter (sub part of turn)
        self.pc = 0
        #: The pickles cursor
        self.cursor = -1
        while 1:
            # Accept key events from the terminal
            key = stdscr.getch()
            #if key != -1:
                #self.debug.write("Got key {}\n".format(key))
            if key == curses.KEY_UP:
                #self.debug.write("Got key up")
                self.game.cursor_up()
            elif key == curses.KEY_DOWN:
                #self.debug.write("Got key down")
                self.game.cursor_down()
            elif key == curses.KEY_LEFT:
                #self.debug.write("Got key left")
                self.game.cursor_left()
            elif key == curses.KEY_RIGHT:
                #self.debug.write("Got key right")
                self.game.cursor_right()
            elif key == 9: #Tab
                #self.debug.write("Got key tab")
                self.game.cursor_hide()
            elif key == 27:
                break
            elif key == 113: #W
                self.unit.cursor_next()
            elif key == 119: #Q
                self.unit.cursor_previous()
            elif key == 32: #Space
                if self.halting:
                    break
                self.paused = not self.paused
                if self.paused:
                    # Create a pickle when we pause.
                    self.debug.write("-- Paused\n")
                    self.pickle(destroy=True)
                else:
                    # Restore the last pickle point when we unpause
                    # Then destroy it.
                    pickle = self.pickles[-1]
                    if pickle['destroy']:
                        self.pickles.pop()
                    self.unpickle(pickle)
                    self.debug.write("-- Unpaused\n")
            elif key == 44: #Left bracket
                if not self.paused:
                    if not self.halting:
                        self.debug.write("--Paused\n")
                    self.pickle(destroy=True)
                    self.paused = True
                    self.cursor = -1
                    self.unpickle(self.pickles[self.cursor])
                else:
                    try:
                        self.cursor -= 1
                        self.unpickle(self.pickles[self.cursor])
                    except IndexError:
                        self.debug.write("--At oldest state\n")
                        self.cursor += 1
            elif key == 46: # Right bracket
                if self.paused:
                    self.cursor += 1
                    if self.cursor > -1:
                        self.debug.write("--At Newest state, unpause to get more tokens.\n")
                        self.cursor = -1
                    try:
                        self.unpickle(self.pickles[self.cursor])
                    except IndexError:
                        self.debug.write("--At Newest state\n")
                    
                
            # Pull items from the pipe if not paused
            if not self.paused:
                try:
                    (t, contents) = self.queue.get(False)
                    if t == 'units':
                        self.game.update(contents)
                    elif t == 'debug':
                        self.debug.write(contents)            
                    elif t == 'halt':
                        self.halting = True
                        self.debug.write("-- End of queue, press space to close\n")
                    elif t == 'breakpoint':
                        if self.tc < contents:
                            self.tc = contents
                            self.pc = 0
                        self.pickle()
                        self.debug.write("-- Breakpoint {}\n".format(contents))
                        self.paused = True
                    elif t == 'snapshot':
                        if self.tc < contents:
                            self.tc = contents
                            self.pc = 0
                        self.pickle()                
                except Empty:
                    pass
                
            #Update the unit view
            self.unit.view(self.game.objects_at_cursor())
            self.debug.blit()
            self.unit.blit()
            self.game.blit()
            sleep(.01)
    
        while not self.halting:
            try:
                (t, contents) = self.queue.get(False)
                if t == 'halt':
                    self.halting = True
            except Empty:
                pass

    def pickle(self,destroy=False):
        self.pc += 1
        pickle = {'debug': self.debug.pickle(), 'unit': self.unit.pickle(), 'game': self.game.pickle(), 'destroy': destroy, 'id': (self.tc,self.pc)}
        self.game.set_snapshot_id(self.tc,self.pc)
        self.pickles.append(pickle)
    
    def unpickle(self,p):
        self.debug.unpickle(p['debug'])
        self.unit.unpickle(p['unit'])
        self.game.unpickle(p['game'])

class CursesWindow(object):
    """
    A generic base class for a curses window.
    """
    def __init__(self,windowbox,border=True,window_title=None):
        #: Intialize the window from the windowbox.
        self.window = windowbox.create()
        if border:
            self.window.border()
            self.window.touchwin()
            if window_title:
                self.window.addstr(0,1,window_title)
            #: The usable in terms of the number of cols
            self.usablex = (1,windowbox.width-1)
            #: The usable space in terms of the number of lines
            self.usabley = (1,windowbox.height-1)
        else:
            self.usablex = (0,windowbox.width)
            self.usabley = (0,windowbox.height)
        self.window.refresh()        
    def blit(self):
        """
        The function which is called every refresh period to redraw the screen.
        """
        self.window.refresh()
    def usable_width(self):
        """
        The usable width of the screen in terms of the number of cols available.
        """
        return self.usablex[1]-self.usablex[0]
    def usable_height(self):
        """
        The usable number of line for a window.
        """
        return self.usabley[1]-self.usabley[0]

    def pickle(self):
        return {}

    def unpickle(self,p):
        pass

class MapWindow(CursesWindow):
    """
    The grid based view of the game map.
    """
    
    def __init__(self, windowbox, colors, mapwidth, mapheight):
        x = super(MapWindow, self).__init__(windowbox,window_title="Map")
        #: The pickle counter of the map being shown
        self.pc = 0
        #: The turn counter of the map map being shown
        self.tc = 0
        self.window.idlok(1)
        self.window.scrollok(True)
        for i in range(mapwidth):
            self.window.addch(2,i*2+4,str(i/10)[0])
            self.window.addch(3,i*2+4,str(i%10)[0])
        for i in range(mapheight):
            self.window.addch(i+4,1,str(i/10)[0])
            self.window.addch(i+4,2,str(i%10)[0])
        self.usablex = (4,self.usablex[1])
        self.usabley = (4,self.usabley[1])
        #: The derived window of the main one where the actual map is drawn
        self.dwindow = self.window.derwin(self.usable_height(),self.usable_width(),self.usabley[0],self.usablex[0])
        self.dwindow.idlok(1)
        self.dwindow.scrollok(True)
        self.dwindow.refresh()
        #: The cursor for selecting a cell in the map
        self.cursor = (0,0)
        #: Should the cursor appear at all
        self.showcursor = False
        #: Is the cursor currently visible, toggled to make it blink
        self.blinkcursor = False
        #: The color scheme
        self.colors = colors
        #: The last time the cursor blinked
        self.lastblink = datetime.today()
        #: The derived window where we right the cursor information
        self.cwindow = self.window.derwin(1,self.usable_width(),1,self.usablex[0])
        self.describe_cursor()
        self.window.refresh()
        #: The width of the map in cols.
        self.mapwidth = mapwidth
        #: The height of the map in lines
        self.mapheight = mapheight
        #: The objects drawn on the map.
        self.objects = []
        return x

    def set_snapshot_id(self,tc,pc):
        self.tc = tc
        self.pc = pc

    def objects_at_cursor(self):
        """
        Returns the objects that are under the map cursor.
        """
        return [ x for x in self.objects if x['x'] == self.cursor[1] and x['y'] == self.cursor[0] ]

    def update(self,objs):
        """
        Updates the objects that will be drawn on the map. 
        
        The function expects a list of dictionaries. The dictionary expects the
        keys x,y and v. v is a tuple which describes how the the object should
        be drawn on the map. The key v will not be shown as part of the unit
        debugger.
        """
        # expects a list of dicts, each of which need and x,y pair
        self.objects = objs

    def blit(self):
        """
        Blit handles the periodic refresh of the map as part of the main
        processing loop. Only the actual grid contents are rewritten since
        they are drawn on a derived window.
        
        This function also draws a cursor on the map, which blinks at a rate
        governed by MAP_CURSOR_BLINK_RATE
        """
        self.describe_cursor()
        self.dwindow.erase()  
        # Draw dots in for all the celles
        for i in range(self.mapwidth):
            for j in range(self.mapheight):
                self.dwindow.addch(j,i*2,'.')
        for o in self.objects:
            self.dwindow.addch(o['y'], o['x']*2, o['v'][0], self.colors.get_color(o['v'][1]))
        if datetime.today()-self.lastblink > MAP_CURSOR_BLINK_RATE:
            self.lastblink = datetime.today()
            self.blinkcursor = not self.blinkcursor
        if self.showcursor and self.blinkcursor:
            self.dwindow.addch(self.cursor[0],self.cursor[1]*2,'*', self.colors.get_color('CURSOR_COLOR'))
        self.dwindow.refresh()
 
    def describe_cursor(self):
        """
        Creates a string describing the current position of the cursor
        which is printed at the top of the map.
        """
        self.cwindow.erase()
        self.cwindow.addstr("Cursor Position {},{} | Showing {}".format(self.cursor[1],self.cursor[0],(self.tc,self.pc)))
        self.cwindow.refresh()
 
    def fix_cursor(self):
        """
        Keeps the cursor within the bound of the map.
        """
        if self.cursor[1] >= self.mapwidth:
            x = 0
        elif self.cursor[1] < 0:
            x = self.mapwidth-1
        else:
            x = self.cursor[1]
        if self.cursor[0] >= self.mapheight:
            y = 0
        elif self.cursor[0] < 0:
            y = self.mapheight-1
        else:
            y = self.cursor[0]
        self.cursor = (y,x)
        self.showcursor = True

    def cursor_left(self):
        """
        A cursor left event.
        """
        self.cursor = (self.cursor[0],self.cursor[1]-1)
        self.fix_cursor()
        return self.cursor

    def cursor_right(self):
        """
        A cursor right event.
        """
        self.cursor = (self.cursor[0],self.cursor[1]+1)
        self.fix_cursor()
        return self.cursor

    def cursor_up(self):
        """
        A cursor up event.
        """
        self.cursor = (self.cursor[0]-1,self.cursor[1])
        self.fix_cursor()
        return self.cursor
    def cursor_down(self):
        """
        A cursor down event
        """
        self.cursor = (self.cursor[0]+1,self.cursor[1])
        self.fix_cursor()
        return self.cursor
    def cursor_hide(self):
        """
        Hides the cursor
        """
        self.showcursor = False

    def pickle(self):
        return {'objects': list(self.objects), 'tc': self.tc, 'pc': self.pc}

    def unpickle(self,pickle):
        self.objects = pickle['objects']
        self.tc = pickle['tc']
        self.pc = pickle['pc']

class UnitWindow(CursesWindow):
    """
    A window which allows you examine units on the map.
    """

    def __init__(self, windowbox):
        x = super(UnitWindow, self).__init__(windowbox,window_title="Unit Viewer")
        self.window.idlok(1)
        self.window.scrollok(True)
        self.window.addstr(1,1,"Press arrow keys to move cursor. Space to pause/unpause output.")
        self.window.addstr(2,1,"Tab will hide the cursor, Q/W cycles through units under the cursor.")
        self.usabley = (3,self.usabley[1])
        #: A derived window where the unit data is written
        self.dwindow = self.window.derwin(self.usable_height(),self.usable_width(),3,1)
        self.window.refresh()
        self.dwindow.idlok(1)
        self.dwindow.scrollok(True)
        self.dwindow.refresh()
        #: The cursor used to track the state
        self.cursor = 0
        #: The id of the object under the cursor to try and track it when the
        #: objects at the cursor change
        self.cursorid = None
        #: The objects that are being viewed constantly
        self.viewing = []
        return x

    def pickle(self):
        return {}
        
    def unpickle(self, p):
        pass

    def view(self,objs):
        """
        Accepts a list of dictionaries to view. Tries to find an object with
        the same id as the old object (if the id key exists) and sets the
        cursor to that object.
        """
        # for simplicity, and pickles, expects a dict
        if self.viewing != objs:
            self.viewing = objs
            self.cursor = 0
            ocid = self.cursorid
            self.cursorid = None
            #We'll try and restore the cursor based on the last object id
            #We looked at, if we can't its no big deal.
            #If the ocid hasn't been set, try to set it to the first obj
            if ocid == None and len(objs) > 0:
                try:
                    self.cursorid = objs[0]['id']
                except KeyError:
                    pass
            #If there are objects and the ocid is set try to restore the cursor
            elif len(objs) > 0:
                c = 0
                for o in objs:
                    try:
                        if o['id'] == ocid:
                            self.cursor = c
                            self.cursorid = o['id']
                    except KeyError:
                        pass
                    c += 1
            #if no matches were found, the cursor will be reset to 0 and the
            #cursorid will be set to the first object, if it has an id:
            if self.cursorid == None and len(objs) > 0:
                try:
                    self.cursorid = objs[0]['id']
                except KeyError:
                    pass
            #All else fails,cursor id returns to the first object
                 
    def cursor_next(self):
        """
        Advances the cursor to the next object and resets the cursorid if the
        id key is available.
        """
        self.cursor += 1
        if self.cursor >= len(self.viewing):
            self.cursor = 0
            try:
                self.cursorid = self.viewing[self.cursor]['id']
            except KeyError:
                pass
            except IndexError:
                pass

    def cursor_previous(self):
        """
        Advances the cursor to the previous object and resets the cursorid if the
        id key is available.
        """
        self.cursor -= 1
        if self.cursor < 0:
            self.cursor = max(0,len(self.viewing)-1)
            try:
                self.cursorid = self.viewing[self.cursor]['id']
            except KeyError:
                pass
            except IndexError:
                pass
    
    def blit(self):
        """
        Handles the main redraw even for the unit viewer. Writes the number
        of objects under the cursor and the currently viewed object.

        This writes all keys of the input dict except those in
        UNIT_KEY_BLACKLIST
        """
        self.dwindow.erase()
        if len(self.viewing) > 0:
            self.dwindow.addstr(0,0,"Viewing unit {}/{}".format(self.cursor+1,len(self.viewing)))
        if len(self.viewing) == 0:
            self.dwindow.refresh()
            return
        c = 1
        for (k,v) in self.viewing[self.cursor].iteritems():
            if c > self.usable_height():
                break
            if k in UNIT_KEY_BLACKLIST:
                continue
            self.dwindow.addstr(c,0,"{}: {}".format(k,v))
            c += 1
        self.dwindow.refresh()


class DebugWindow(CursesWindow):
    """
    The window which shows the regular stderr and stdout output so you can have
    whatever sort of debug you'd like for your program.
    """
    
    def __init__(self, windowbox, scrollback=2000):
        x = super(DebugWindow, self).__init__(windowbox,window_title="Debug Output")
        self.window.refresh()
        #: The history of lines
        self.dwindow = self.window.derwin(self.usable_height(),self.usable_width(),1,1)
        self.dwindow.idlok(1)
        self.dwindow.scrollok(True)
        self.dwindow.refresh()
        self.scrollback = []
        self.scrollbacklines = scrollback
        self.write("Logger Output Will Appear Here\n")
        return x

    def pickle(self):
        return {'scrollback': list(self.scrollback)}

    def unpickle(self, p):
        self.scrollback = p['scrollback']
        self.dwindow.erase()
        self.dwindow.refresh()
        for line in self.scrollback:
            self.dwindow.addstr(line)
        self.dwindow.refresh()

    def write(self,string):
        """
        Puts a string to the screen.
        """
        string = str(string)
        self.scrollback.append(string)
        while len(self.scrollback) > self.scrollbacklines:
            self.scrollback.pop(0)
        #Chunk the string to display nicely:
        self.dwindow.addstr(string)
        self.dwindow.refresh()

