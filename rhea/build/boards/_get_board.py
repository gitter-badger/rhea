# Copyright (c) 2014 Christopher Felton
#

from __future__ import division
from __future__ import print_function

from .xilinx._xula import Xula, Xula2
from .xilinx._papilio import Pone

from .altera._de0nano import DE0Nano
from .altera._de0nano_soc import DE0NanoSOC

xbrd = {
    'xula': Xula,
    'xula2': Xula2,
    'pone': Pone,
}

abrd = {
    'de0nano': DE0Nano,
    'de0nano_soc': DE0NanoSOC,
}

def get_board(name):
    """ retrieve a board definition from the name provided.
    """
    brd = None
    if xbrd.has_key(name):
        brd = xbrd[name]()
    elif abrd.has_key(name):
        brd = abrd[name]()
    else:
        # @todo: print out a list of boards and descriptions
        raise ValueError("Invalid board %s"%(name,))
    
    return brd
