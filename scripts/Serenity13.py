#!/usr/bin/python

import logging
import pickle
import sys
import re
import time
import snap7
import struct
import colorsys
import os
import socket
import datetime
from bs4 import BeautifulSoup
import sys
import urllib2
import requests


def readtemp(address,sensor):
  stream = os.popen('ssh root@192.168.0.2 "clia sensordata '+address+' 0:'+sensor+'|grep Processed|cut -b 21-25"')
  #stream = os.popen('ipmitool -H 192.168.0.2 -P "" -t '+address+' sensor|grep "'+sensor+'"|cut -b 20-25')
  #stream = os.popen('ipmitool -H 10.0.0.21 -P "" sensor|grep "'+sensor+'"|cut -b 20-25')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  #print(sensor+ " "+temp_cc.strip())
  if temp_cc.strip()=="na": 
    return "na"
  return float(temp_cc.strip())

PIM400KZ_temp=readtemp("90","5")
PIM400KZ_current=readtemp("90","6")
PIM400KZ_voltageA=readtemp("90","7")
PIM400KZ_voltageB=readtemp("90","8")
X0FPGATEMP = readtemp("90","3")
X1FPGATEMP = readtemp("90","4")

#internal_temp=readtemp("92","3")
#U34_temp=readtemp("92","4")
#U35_temp=readtemp("92","5")
#U36_temp=readtemp("92","6")
#CMuM_temp=readtemp("92","7")
#Firefly_temp=readtemp("92","8")
#CM_FPGA_temp=readtemp("92","9")
#CM_regulator_temp=readtemp("92","10")

timestamp = time.time()

dblist = []
if PIM400KZ_temp!="na": dblist.append(["serenity13.temperatues.PIM400KZ_temp", ( timestamp, PIM400KZ_temp) ])
if PIM400KZ_current!="na": dblist.append(["serenity13.temperatues.PIM400KZ_current", ( timestamp, PIM400KZ_current) ])
if PIM400KZ_voltageA!="na": dblist.append(["serenity13.temperatues.PIM400KZ_voltageA", ( timestamp, PIM400KZ_voltageA) ])
if PIM400KZ_voltageB!="na": dblist.append(["serenity13.temperatues.PIM400KZ_voltageB", ( timestamp, PIM400KZ_voltageB) ])
if X0FPGATEMP!="na": dblist.append(["serenity13.IPMC.X0FPGATEMP", ( timestamp, X0FPGATEMP) ])
if X1FPGATEMP!="na": dblist.append(["serenity13.IPMC.X1FPGATEMP", ( timestamp, X1FPGATEMP) ])


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

