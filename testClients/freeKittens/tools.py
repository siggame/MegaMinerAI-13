__author__ = 'Tarnasa'


def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def inrange(x1, x2, x):
    return x1 <= x <= x2


def inbox(x1, y1, x2, y2, x, y):
    return inrange(x1, x2, x) and inrange(y1, y2, y)