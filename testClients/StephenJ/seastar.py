from ctypes import *
import os

class Seastar(object):
    """
    Python code to interface with my C based A*
    """
    def __init__(self, map_width, map_height):
        """
        Calls the library's init astar function that prepares the adjacency
        table. You can call it a bunch of times, but it just wastes CPU.
        
        Also initializes the blocking and obstacles to some default settings.
        """
        try:
          if os.name == 'posix':
            self.library = CDLL("./libseastar.so")
          else:
            raise Exception("Unrecognized OS: "+os.name)
        except OSError:
          raise Exception("It looks like you didn't build libclient. Run 'make' and try again.")

        self.library.init_astar.argtypes = [c_int, c_int]
        
        self.library.astar.argtypes = [POINTER(c_int), c_int, POINTER(c_int), c_int,
            POINTER(c_int), c_int, c_int]
        self.library.astar.restype = POINTER(c_int)

        self.library.freepath.argtypes = [POINTER(c_int)]

        self.library.init_astar(c_int(map_width), c_int(map_height))

        self.map_width = map_width
        self.map_height = map_height

        # Init: no obstacles
        self.obstacles = [ 0 for _ in range(map_width * map_height) ]
        self.build_cobstacles()

        # Init: Everything blocks a path.
        self.set_blocking(0xffffffff) # Block on any obstacle
        
        # To save CPU, we will burn the xy to index list to a list
        self.indextoxy = [ (x%map_width, x/map_width) for x in range(map_width*map_height) ]
        self.xytoindex = [ list() for x in range(map_width) ]
        for x in range(map_width):
            self.xytoindex[x] = [ x+y*map_width for y in range(map_height) ]

    def xytuples_to_clist(self, lst):
        """
        Given a list of tuples, this function converts it to the flat c_type
        int array used by the c based astar
        """
        clength = len(lst)
        cltype = c_int * clength
        outlst = [ self.xytoindex[x][y] for (x,y) in lst ]
        return cltype(*outlst)

    def clist_to_xytuples(self, lst, length=None):
        """
        Given a flat c_type int array of points, convert it to a list of tuples
        with the method based on if you know how long the array is.
        """ 
        if length != None:
            # Apply the length to the clist, which may or may not alread have a
            # size:
            resize(lst,length * sizeof(c_int))
            i = 0
            for i in range(length):
                yield self.indextoxy[ int(lst[i]) ]
        else:
            # We don't know what the length of the list is. We have to expand
            # The list and then search through the memory, wee!
            i = 0
            while lst[i] != -1:
                yield self.indextoxy[ int(lst[i]) ]
                i += 1

    def set_blocking(self,blk):
        """
        Changes the blocking mask that will be used in the next pathing.
        """
        self.blocking = blk
        self.c_blocking = c_int(blk)

    def build_cobstacles(self):
        """
        Converts the python obstacle map to the ctype array that init_astar
        can use.
        """
        clength = len(self.obstacles)
        cotype = c_int * clength
        self.c_obstacles = cotype(*self.obstacles)
        self.c_obstacles_dirty = False

    def reset_obstacles(self,layer=0xffffffff):
        """
        Given a layer mask, remove all the obstacles from that layer.
        """
        for i in range(len(self.obstacles)):
            self.obstacles[i] = self.obstacles[i] & ~layer
        self.c_obstacles_dirty = True

    def add_obstacles(self, lst, layer):
        """
        Given a list of x,y tuples and a layer mask, add obstacles to those
        layers.
        """
        for (x,y) in lst:
            index = self.xytoindex[x][y]
            self.obstacles[index] = self.obstacles[index] | layer
        self.cobstacles_dirty = True

    def add_mappables(self, lst, layer):
        lst = ( (item.getX(), item.getY()) for item in lst )
        self.add_obstacles(lst, layer)

    def get_path(self, starts, ends):
        """
        Tries to find a path between one of the starts and ends. Returns the
        shortest path between one of the starts and one of the ends. Returns
        an empty list if no path is found. Otherwise, returns a list of x,y
        tuples which are the path.

        C function args:
        -list of start points
        -count of start points
        -list of end points
        -count of end pints
        -list of obstacles
        -count of obstacles
        -blocking mask.
        """
        if self.c_obstacles_dirty:
            # The obstacles have changed since the last run, we have to
            # rebuild the layer:
            self.build_cobstacles()
        c_starts = self.xytuples_to_clist(starts)
        c_starts_c = c_int(len(starts))
        c_ends = self.xytuples_to_clist(ends)
        c_ends_c = c_int(len(ends))
        c_obstacles_c = c_int(self.map_width*self.map_height)
        rslt = self.library.astar(c_starts, c_starts_c, c_ends, c_ends_c,
            self.c_obstacles, c_obstacles_c, self.c_blocking)
        if not rslt:
            return []
        r = list(self.clist_to_xytuples(rslt))
        self.library.freepath(rslt)
        return r
