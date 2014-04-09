def buildorder(ai):
    while 1:
        yield (1, None)
        yield (3, None)
    while 1:
        bases = set([ (x.getX(), x.getY()) for x in ai.mybases ])
        walls = set([ (x.getX(), x.getY()) for x in ai.mywalls ])
        dropping = set([ (x.getX(), x.getY()) for x in ai.droppingtiles ])
        wallpts = set()
        for tile in bases:
            tmp = [ (tile[0]+1,tile[1]),
                    (tile[0]-1,tile[1]),
                    (tile[0],tile[1]+1),
                    (tile[0],tile[1]-1) ]
            for t in tmp:
                if t not in bases and t not in dropping:
                    wallpts.add(t)
        wallpts -= walls
        for location in wallpts:
            yield (5, location)
        else:
            yield (1, None)
