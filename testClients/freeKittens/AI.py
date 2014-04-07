#-*-python-*-
from BaseAI import BaseAI

from make_kittens import *
from play import *
from cat_vision import *
from cat_scan import *

class AI(BaseAI):
    """The class implementing gameplay logic."""
    @staticmethod
    def username():
        return "Free kittens"

    @staticmethod
    def password():
        return "password"

    ##This function is called once, before your first turn
    def init(self):
        pass

    ##This function is called once, after your last turn
    def end(self):
        pass

    ##This function is called each time it is your turn
    ##Return true to end your turn, return false to ask the server for updated information
    def run(self):
        cat_scan(self)
        make_kittens(self)
        play(self)
        show_cat(cat_see(self))
        return 1


def __init__(self, conn):
    BaseAI.__init__(self, conn)
