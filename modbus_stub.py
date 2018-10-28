#!/usr/bin/env python -u

"""
2018-10-27
Requirements:
    git clone https://github.com/ljean/modbus-tk.git
    cd modbus-tk
    sudo python3 setup.py install
    cd ~

Usage:
    sudo python3 modbus_stub.py
"""

import sys
import time
from math import pi
import struct
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp

def mb_set_float(addr, val):
    j = struct.unpack('<HH',struct.pack('<f', val))
    slave_1.set_values('ro', addr, j)
    return val

def mb_get_float(addr):
    i2, i1 = slave_1.get_values('ro', addr, 2)
    return struct.unpack('>f',struct.pack('>HH',i1,i2))[0]

if __name__ == "__main__":
    try:
        """ Initialize the MODBUS TCP slave """        
        mb_start = 40001
        mb_len = 2
        server = modbus_tcp.TcpServer(address='0.0.0.0')
        server.start()
        slave_1 = server.add_slave(1)
        slave_1.add_block('ro', cst.HOLDING_REGISTERS, mb_start, mb_len)
        """ 
        modpoll -0 -1 -m tcp -t 4:float -r 40001 -c 1 -o 3 192.168.x.x

        -0          First reference is 0 (PDU addressing) instead 1
        -1          Poll only once, otherwise poll every second
        -m tcp      MODBUS/TCP protocol
        -t 4:float  32-bit float data type in output (holding) register table
        -c 1        Number of values to poll (1-100, 1 is default)
        -o 3        Time-out in seconds (0.01 - 10.0, 1.0 s is default)
        """
    
        print("Ready")

        while True:
            """
            40001   Quality Control (3.14159265359)            
            """
            mb_set_float(40001, pi)  
            print(mb_get_float(40001))                                    
            time.sleep(1)

    finally:
        server.stop()
