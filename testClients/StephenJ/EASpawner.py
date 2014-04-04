import random
import json

VALID_SPAWNS = [ 0, 1, 2, 3, 6 ]

MUTATE_RATE_DELETE = 0.10
MUTATE_RATE_INSERT = 0.10
MUTATE_RATE_DUPLICATE = 0.05

MAX_POOL_SIZE = 50

RANDOM_MIN_LENGTH = 1
RANDOM_MAX_LENGTH = 500

def save_buildorder(fname, buildorder):
    fp = open(fname,'w')
    for item in buildorder:
        fp.write("{}\n".format(item))

def combine_buildorders(o1, o2):
    t1 = list(o1)
    t2 = list(o2)
    while len(t1) < len(t2):
        t1.append(None)
    while len(t2) < len(t1):
        t2.append(None)
    z = zip(t1,t2)
    r = []
    for item in z:
        c = random.choice(item)
        if c != None:
            r.append(c)
    return r

def mutate_delete(lst,n):
    lst = list(lst)
    for _ in range(n):
        index = range(len(lst))
        c = random.choice(index)
        lst.pop(c)
    return lst

def mutate_insert(lst,n):
    lst = list(lst)
    for _ in range(n):
        index = range(len(lst))
        lst.insert(index, random.choice(VALID_SPAWNS))
    return lst
        
def mutate_duplicate(lst, n1, n2):
    lst = list(lst)
    sli = lst[n1:n2]
    return lst + sli

class Candidate(object):
    def __init__(self,combine=None):
        self.order = []
        self.wins = 0
        self.losses = 0
        self.games = 0
        
        if combine == None:
            length = random.randint(RANDOM_MIN_LENGTH, RANDOM_MAX_LENGTH)
            for i in range(length):
                self.order.append(random.choice(VALID_SPAWNS))
        else:
            (c1,c2) = combine
            self.order = combine_buildorders(c1.order, c2.order)

    def to_file(self, fname):
        save_buildorder(fname, buildorder)

    def to_json(self, fname):
        d = {'order': self.order,
             'wins': self.wins,
             'losses': self.losses,
             'games': self.games}
        fp = file(fname,'w')
        json.dump(fp, d)


