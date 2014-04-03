from screen import *
import sys

from multiprocessing import Process, Queue, Value
import curses
from time import sleep
from datetime import datetime, timedelta
from StringIO import StringIO
from Queue import Empty
import traceback
import os

import random


class Vexulizer(object):
    """
    The parent object responsible for launching the curses interface and making
    all the appropriate changes to the output buffers & such. This object spawns
    the curses screen as part of its startup behavior.
    """
    #: A static member which holds the real stdout for restoring it.
    rstdout = sys.stdout
    #: A static member which holds the real stderr for restoring it.
    rstderr = sys.stderr

    def __init__(self,mapwidth,mapheight):
        """
        Constructor for the vexulizer, given a mapwidth and mapheight this
        spawns the curses process and redirects stdout and stderr to prevent
        them from mucking up the curses, while still presenting them to the
        end user
        """
        #: The the multiprocess queue used to deliver tokens to curses
        self.locq = Queue()
        #: A boolean to indicate that the curses screen is active and has
        #: not crashed
        self.mapwidth = mapwidth
        self.mapheight = mapheight    

    def stop_debugger(self):
        """
        This function will end the debugger by putting a halt token in to the
        queue. A halt token will make the debugger stop processing tokens and
        end the display.

        Afterwards, when the visualizer has joined, we will flush the queue of
        tokens, because a non-empty queue causes a nasty hang on exit. Lastly,
        stdout and stderr are restored.
        """
   
        self.running = Value('b',True)
        screen = AsyncCursesScreen(self.mapheight,self.mapwidth)
        #: The process spawned for curses
        self.proc = Process(target=screen.start, args=(self.locq,self.running))
        #: The buffer which will capture stdout contents
        self.buff = DebugBuffer(self.locq,self.running,sys.stdout)
        #: The buffer which will capture stderr contents
        self.errbuff = DebugBuffer(self.locq,self.running,sys.stderr)
        self.proc.start()
        sys.stdout = self.buff
        sys.stderr = self.errbuff

        self.locq.put(('halt',''),False)
        if not self.running.value:
            self.proc.terminate()
            # If the local queue is not empty the process will hang on exit
            # so dump the queue out
        self.proc.join()
        try:
            while 1:
               self.locq.get(False)
        except Empty:
            pass
        self.rstdout.write(sys.stdout.getvalue())
        self.rstderr.write(sys.stderr.getvalue())
        sys.stdout = self.rstdout
        sys.stderr = self.rstderr
        sys.stdout.flush()
        sys.stderr.flush()   
 
    def update_units(self, units):
        """
        Function to transport the units token to the curses screen.
        """
        self.locq.put(('units',units))
    
    def mark_turn(self, turn):
        self.locq.put(('snapshot',turn))

    def print_debug(self, string):
        """
        Function to directly access the print function of the curses screen
        without routing through the debug buffers.
        """
        self.locq.put(('debug',string))

class DebugBuffer(StringIO):
    """
    An extension of StringIO which intends to capture and redirct input from
    things such as print (or direct writes to sys.stdout) and converts them to
    tokens for displaying on the vexulizer.) It captures all the tokens it
    consumes, which allows the content to be restored on exit.
    
    StringIO is an old style class so I couldn't use super()
    """
    def __init__(self,locq,running, replaces=None):
        #: The queue tokens will be placed in
        self.locq = locq
        #: The value indicating if the curses screen is running
        self.running = running
        #: The buffer this replaces.
        self.replaces = replaces
        StringIO.__init__(self)
    
    def write(self,s):
        """
        A call to write will put the contents of the input string (s) into the
        underlying stringIO object and then determine if the curses screen is
        active. If it isn't, the output it sent the buffer this object originally
        overwrote.
        """
        StringIO.write(self,s)
        if not self.running.value and self.replaces:
            self.replaces.write(s)
            self.replaces.flush()
        else:
            self.locq.put(('debug',s))
    
    def writelines(self,sequence):
        """
        A call to write will put the contents of the input sequence into the
        underlying stringIO object and then determine if the curses screen is
        active. If it isn't, the output it sent the buffer this object originally
        overwrote.
        """
        StringIO.writelines(self,sequence)
        if not self.running.value and self.replaces:
            self.replaces.writelines(sequence)
            self.replaces.flush()
        else:
            for line in sequence:
                self.locq.put(('debug',line))


if __name__ == "__main__":
    v = Vexulizer(40,20)

    print "Goodbye"
    print "You Say Hello"
    print "I say goodbye"

    print "This is a particularly long string: it is interesting because magically, it will make" \
        "me cry out to thor and summon him forth"

    for i in range(10):
        print "Turn {}".format(i)
        #v.print_debug(locq,"Hello world!!") 
        mapjunk = []
        for j in range(200): 
            mapjunk.append({'x':random.randint(0,40-1),
                            'y':random.randint(0,20-1),
                            'v':random.choice([('X','WALL_COLOR'),
                                               ('W','ENEMY_COLOR'),
                                               ('W','MY_COLOR'),
                                               ('S','ENEMY_COLOR'),
                                               ('S','MY_COLOR')]),
                            'health': random.randint(1,100),
                            'id': j,
                            'attacks': random.randint(0,3)
                            })
        #Convert the string IO to print debug
        print "Test!"
        v.update_units(mapjunk)
        v.mark_turn(i)
        sleep(.5)
 
    v.stop_debugger()
