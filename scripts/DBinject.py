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
  return float(temp_cc)

def readrpm(address):
  stream = os.popen('ssh root@192.168.0.2 "clia sensordata '+address+' 0:10|grep Processed|cut -d \' \' -f 7 "')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  return temp_cc.rstrip()

def readexttemp():
  stream = os.popen('ssh root@192.168.0.2 "clia sensordata 10 0:2|grep Processed|cut -b 21-25"')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  return float(temp_cc)

def rangeconv(trange_i, value_i):
  if value_i<trange_i[0]:
    return 200
  if value_i>trange_i[1]:
    return 0
  return 100-int( (value_i-trange_i[0])/(trange_i[1]-trange_i[0])*100. )

def rangeinv(trange_i, value_i):
  return int(trange_i[0]+(trange_i[1]-trange_i[0])*(100-value_i)/100)


def getsnmp(address):
  stream = os.popen('snmpwalk  -v2c -c public 192.168.0.20 '+address+' |cut -d " " -f 4')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  return float(temp_cc.rstrip())   


#url = 'http://192.168.0.10/status.xml'
#username = 'meanwell'
#password = 'meanwell'
#html_doc = requests.get(url, auth=(username, password)).content

#soup = BeautifulSoup(html_doc, 'xml')
#PSU_power = soup.find_all('Current0')[0].get_text()

PSU_current = getsnmp("enterprises.12148.10.5.2.5.0")/10
#PSU_current = getsnmp("enterprises.12148.10.10.6.5.0")/100
PSU_voltage = getsnmp("enterprises.12148.10.10.5.5.0")/100
PSU_power=PSU_current*PSU_voltage

lower_left=0#readtemp("5a","7")
lower_center=0#readtemp("5a","8")
lower_right=0#readtemp("5a","9")
upper_left=0#readtemp("5c","6")
upper_center=0#readtemp("5c","7")
upper_right=0#readtemp("5c","8")
external=0#readexttemp()
rpmlower=0#readrpm("5a")
rpmupper=0#readrpm("5c")

timestamp = time.time()

dblist = []
dblist.append(["shelf.temperatures.fantray.LowerLeft", ( timestamp, lower_left ) ])
dblist.append(["shelf.temperatures.fantray.LowerCenter", ( timestamp, lower_center ) ])
dblist.append(["shelf.temperatures.fantray.LowerRight", ( timestamp, lower_right ) ])
dblist.append(["shelf.temperatures.fantray.UpperLeft", ( timestamp, upper_left ) ])
dblist.append(["shelf.temperatures.fantray.UpperCenter", ( timestamp, upper_center ) ])
dblist.append(["shelf.temperatures.fantray.UpperRight", ( timestamp, upper_right ) ])
dblist.append(["shelf.temperatures.external", ( timestamp, external ) ])
dblist.append(["shelf.fanspeed.fantray.LowerFanTray", ( timestamp, rpmlower ) ])
dblist.append(["shelf.fanspeed.fantray.UpperFanTray", ( timestamp, rpmupper ) ])
dblist.append(["PSU.current", ( timestamp, PSU_current ) ])
dblist.append(["PSU.voltage", ( timestamp, PSU_voltage ) ])
dblist.append(["PSU.power", ( timestamp, PSU_power ) ])



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

