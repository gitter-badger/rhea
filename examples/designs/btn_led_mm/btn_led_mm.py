
from __future__ import print_function

import argparse

from myhdl import *

import rhea.build as build

from rhea.cores.misc import button_controller   # memmap controller
from rhea.cores.misc import led_peripheral      # memmap peripheral

from rhea.system import Global
from rhea.system import Barebone
from rhea.system import Wishbone
from rhea.system import AvalonMM
from rhea.system import AXI4


def m_btn_led_mm(clock, reset, leds, btns, bus_type='W'):
    """ A toy example to demostrate bus agnosticism
    This example instantiates a memory-map controller and a
    memory-map peripheral.  This example shows how the 
    controllers and peripherals can be passed the memmap
    interface.  The passing of the interface allows the 
    modules (components) to be bus agnostic.

    This example solves a simple task in a complicated manner
    to show the point.  When a button press is detected a 
    bus cycle is generated to write the "flash" pattern to 
    the LED peripheral.

    Note: for easy FPGA bit-stream generation the port names
    match the board names defined in the *gizflo* board definitions.
    """
    glbl = Global(clock=clock, reset=reset)

    if bus_type == 'B':
        regbus = Barebone(glbl, data_width=8, address_width=16)
    elif bus_type == 'W':
        regbus = Wishbone(glbl, data_width=8, address_width=16)
    elif bus_type == 'A':
        regbus = AvalonMM(glbl, data_width=8, address_width=16)
    #elif bus_type == 'X':
    #    regbus = AXI4(glbl, data_wdith=8, address_width=16)
    else:
        raise Exception("Invalid bus type {}".format(bus_type))

    gbtn = button_controller(glbl, regbus, btns)  # memmap controller
    gled = led_peripheral(glbl, regbus, leds)     # memmap peripheral
    gmap = regbus.m_per_outputs()                 # bus combiner

    print(vars(regbus.regfiles['LED_000']))

    return gbtn, gled, gmap


def build(args):
    """ Run the FPGA tools
    """
    pass


def getargs():
    """ get CLI arguments
    """
    pass


if __name__ == '__main__':
    args = getargs()
    build(args)
