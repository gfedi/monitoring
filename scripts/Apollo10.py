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
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  if temp_cc=="": 
    return "na"
  return float(temp_cc)

internal_temp=readtemp("9a","3")
U34_temp=readtemp("9a","4")
U35_temp=readtemp("9a","5")
U36_temp=readtemp("9a","6")
CMuM_temp=readtemp("9a","7")
Firefly_temp=readtemp("9a","8")
CM_FPGA_temp=readtemp("9a","9")
CM_regulator_temp=readtemp("9a","10")

timestamp = time.time()

dblist = []
if internal_temp!="na": dblist.append(["apollo10.temperatues.internal_temp", ( timestamp, internal_temp ) ])
if U34_temp!="na": dblist.append(["apollo10.temperatues.U34_temp", ( timestamp, U34_temp ) ])
if U35_temp!="na": dblist.append(["apollo10.temperatues.U35_temp", ( timestamp, U35_temp ) ])
if U36_temp!="na": dblist.append(["apollo10.temperatues.U36_temp", ( timestamp, U36_temp ) ])
if CMuM_temp!="na": dblist.append(["apollo10.temperatues.CMuM_temp", ( timestamp, CMuM_temp ) ])
if Firefly_temp!="na": dblist.append(["apollo10.temperatues.Firefly_temp", ( timestamp, Firefly_temp ) ])
if CM_FPGA_temp!="na": dblist.append(["apollo10.temperatues.CM_FPGA_temp", ( timestamp, CM_FPGA_temp ) ])
if CM_regulator_temp!="na": dblist.append(["apollo10.temperatues.CM_regulator_temp", ( timestamp, CM_regulator_temp ) ])



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

