def buildorder(ai):
    yield (6, None)
    yield (6, None)
    yield (6, None)
    yield (6, None)
    yield (6, None)
    yield (6, None)
    bases = set([ (x.getX(), x.getY()) for x in ai.mybases ])
    wallpts = set()
    for tile in bases:
        tmp = [ (tile[0]+1,tile[1]),
                (tile[0]-1,tile[1]),
                (tile[0],tile[1]+1),
                (tile[0],tile[1]-1) ]
        for t in tmp:
            if t not in bases:
                wallpts.add(t)
    for location in wallpts:
        yield (5, location)
    while 1:
        yield (6, None)
