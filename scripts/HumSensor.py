#!/usr/bin/python3.4

import socket
import pickle
import struct
import serial
import time
from datetime import datetime
import sys
import math
import snap7

    
client = snap7.client.Client()
client.connect('128.141.63.209', 0, 0)
topo = client.db_read(402,36,1)
topo2 = client.db_read(402,44,1)

print(hex(topo[0]), hex(topo2[0]))

print(topo[0]&0b00001, topo2[0]&0b00001)

#for probe in probes:
#      byte_index=probes[probe]
#      x = topo[byte_index:byte_index + 4]
#      temps[probe] = struct.unpack('>f', struct.pack('4B', *x))[0]

