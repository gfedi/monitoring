#!/usr/bin/env python3.6

import struct
import pickle
import socket
import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

client = ModbusClient(method='rtu', port='/dev/ttyUSB0',bytesize=8, stopbits=2,timeout=1,baudrate=19200, parity='N')
client.connect()

def read_register(offset, unit):
  # offset is the ID of variable as written in the table 
  # 2 is the amount of registers read, 2x16 bits variable
  # unit is the RTU address
  response = client.read_holding_registers(offset,2,unit=unit)
  decode = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.Big)
  return decode.decode_32bit_float()

registers = {}
registers["volt1n"] = 1
registers["volt2n"] = 3
registers["volt3n"] = 5
registers["amp1"] = 13
registers["amp2"] = 15
registers["amp3"] = 17
registers["reapow1"] = 31
registers["reapow2"] = 33
registers["reapow3"] = 35
registers["power"] = 65

timestamp = time.time()

dblist = []


#print("***   Unit 1  ****")
for reg in registers:
  dblist.append(["rackA16.ShelfA."+reg, ( timestamp, read_register(registers[reg],0x7e) ) ])
  #print(reg+"=\t\t",(read_register(registers[reg],0x7e)))
#print("***   Unit 2  ****")
for reg in registers:
  dblist.append(["rackA16.ShelfB."+reg, ( timestamp, read_register(registers[reg],0x7f) ) ])
  #print(reg+"=\t\t",read_register(registers[reg],0x7f))


payload = pickle.dumps(dblist, protocol=2)
header = struct.pack("!L", len(payload))
message = header + payload

retrycount = 0
while (retrycount < 10):

  sock = socket.socket()
  sock.settimeout(1)

  try :
    sock.connect(('128.141.49.116', 2004))
    sock.send(message)
    break;

  except (socket.timeout, socket.error) as error:
    logging.error('connect error: %s', error)
    retrycount += 1

sock.close()

