
from __future__ import print_function
from __future__ import absolute_import

import myhdl
from myhdl import instance

# @todo: move "interfaces" to system (or interfaces)
from ...cores.sdram import SDRAMInterface

from ...system import MemMap
from ...system import FIFOBus   # @todo: ustilize FIFOBus


def sdram_controller_model(sdram_intf, internal_intf):
    """ Model the transaction between the internal bus and external SDRAM

    :param sdram_intf: Interface to the SDRAM device
    :param internal_intf: Internal interface
    :return: myhdl generators

    Not convertible.
    """
    assert isinstance(sdram_intf, SDRAMInterface)
    assert isinstance(internal_intf, (MemMap, ))  # @todo: add FIFOBus

    # short-cuts
    ix, ex = internal_intf, sdram_intf

    def translate_address(addr):
        #@todo: add correct translation
        row_addr, col_addr = 0, addr
        return row_addr, col_addr

    @instance
    def mproc():
        """
        Emulated using the interface transactors, performs the
        following:
           - address translation
           - arbitration

        """

        while True:
            addr = ix.get_address()
            row_addr, col_addr = translate_address(addr)
            if ix.is_write:
                data = ix.get_write_data()
                yield ex.write(data, row_addr, col_addr)
                yield ix.ack()
            elif ix.is_read:
                yield ex.read(row_addr, col_addr)
                read_data = ex.get_read_data()
                yield ix.ack(read_data)

            yield ix.clock.posedge

    return mproc
