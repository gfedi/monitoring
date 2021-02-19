#!/usr/bin/python

import logging
import pickle
import sys
import re
import time
import struct
import colorsys
import os
import socket
import datetime
import sys
import urllib2


def readtempA(address,sensor):
  stream = os.popen('ssh root@192.168.0.4 "clia sensordata '+address+' 0:'+sensor+'|grep Processed|cut -b 21-25"')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  return float(temp_cc)


def getsnmpA(address):
  stream = os.popen('snmpwalk  -v2c -c public 192.168.0.22 '+address+' |cut -d " " -f 4')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  return float(temp_cc.rstrip())   

def readtempB(address,sensor):
  stream = os.popen('ssh root@192.168.0.3 "clia sensordata '+address+' 0:'+sensor+'|grep Processed|cut -b 21-25"')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  return float(temp_cc)


def getsnmpB(address):
  stream = os.popen('snmpwalk  -v2c -c public 192.168.0.21 '+address+' |cut -d " " -f 4')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  return float(temp_cc.rstrip())


PSU_current = getsnmpA("enterprises.12148.10.5.2.5.0")/10
PSU_voltage = getsnmpA("enterprises.12148.10.10.5.5.0")/100
PSU_power=PSU_current*PSU_voltage
Rect_temp = getsnmpA("enterprises.12148.10.5.18.5.0")

local_temp = readtempA("10","2")
PEMA_temp = readtempA("20","140")
PEMB_temp = readtempA("20","141")
lower_left=readtempA("5a","7")
lower_center=readtempA("5a","8")
lower_right=readtempA("5a","9")
upper_left=readtempA("5c","6")
upper_center=readtempA("5c","7")
upper_right=readtempA("5c","8")

PSU_currentB = getsnmpB("enterprises.12148.10.5.2.5.0")/10
PSU_voltageB = getsnmpB("enterprises.12148.10.10.5.5.0")/100
PSU_powerB = PSU_currentB*PSU_voltageB
Rect_tempB = getsnmpB("enterprises.12148.10.5.18.5.0")

local_tempB = readtempB("10","2")
PEMA_tempB = readtempB("20","140")
PEMB_tempB = readtempB("20","141")
lower_leftB=readtempB("5a","7")
lower_centerB=readtempB("5a","8")
lower_rightB=readtempB("5a","9")
upper_leftB=readtempB("5c","6")
upper_centerB=readtempB("5c","7")
upper_rightB=readtempB("5c","8")

timestamp = time.time()

dblist = []
dblist.append(["rackA16.ShelfA.localtemp", ( timestamp, local_temp ) ])
dblist.append(["rackA16.ShelfA.PEMA", ( timestamp, PEMA_temp ) ])
dblist.append(["rackA16.ShelfA.PEMB", ( timestamp, PEMB_temp ) ])
dblist.append(["rackA16.ShelfA.fantray.LowerLeft", ( timestamp, lower_left ) ])
dblist.append(["rackA16.ShelfA.fantray.LowerCenter", ( timestamp, lower_center ) ])
dblist.append(["rackA16.ShelfA.fantray.LowerRight", ( timestamp, lower_right ) ])
dblist.append(["rackA16.ShelfA.fantray.UpperLeft", ( timestamp, upper_left ) ])
dblist.append(["rackA16.ShelfA.fantray.UpperCenter", ( timestamp, upper_center ) ])
dblist.append(["rackA16.ShelfA.fantray.UpperRight", ( timestamp, upper_right ) ])
dblist.append(["rackA16.PSUA.current", ( timestamp, PSU_current ) ])
dblist.append(["rackA16.PSUA.voltage", ( timestamp, PSU_voltage ) ])
dblist.append(["rackA16.PSUA.power", ( timestamp, PSU_power ) ])
dblist.append(["rackA16.PSUA.temp", ( timestamp, Rect_temp ) ])

dblist.append(["rackA16.ShelfB.localtemp", ( timestamp, local_tempB ) ])
dblist.append(["rackA16.ShelfB.PEMA", ( timestamp, PEMA_tempB ) ])
dblist.append(["rackA16.ShelfB.PEMB", ( timestamp, PEMB_tempB ) ])
dblist.append(["rackA16.ShelfB.fantray.LowerLeft", ( timestamp, lower_leftB ) ])
dblist.append(["rackA16.ShelfB.fantray.LowerCenter", ( timestamp, lower_centerB ) ])
dblist.append(["rackA16.ShelfB.fantray.LowerRight", ( timestamp, lower_rightB ) ])
dblist.append(["rackA16.ShelfB.fantray.UpperLeft", ( timestamp, upper_leftB ) ])
dblist.append(["rackA16.ShelfB.fantray.UpperCenter", ( timestamp, upper_centerB ) ])
dblist.append(["rackA16.ShelfB.fantray.UpperRight", ( timestamp, upper_rightB ) ])
dblist.append(["rackA16.PSUB.current", ( timestamp, PSU_currentB ) ])
dblist.append(["rackA16.PSUB.voltage", ( timestamp, PSU_voltageB ) ])
dblist.append(["rackA16.PSUB.power", ( timestamp, PSU_powerB ) ])
dblist.append(["rackA16.PSUB.temp", ( timestamp, Rect_tempB ) ])

for entry in dblist:
  print(entry)

payload = pickle.dumps(dblist, protocol=2)
header = struct.pack("!L", len(payload))
message = header + payload

retrycount = 0
while (retrycount < 10):

  sock = socket.socket()
  sock.settimeout(1)

  try :
    sock.connect(('137.138.192.171', 2004))
    sock.send(message)
    break;

  except (socket.timeout, socket.error) as error:
    logging.error('connect error: %s', error)
    retrycount += 1

sock.close()

