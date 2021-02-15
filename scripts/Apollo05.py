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
  #stream = os.popen('ssh root@192.168.0.2 "clia sensordata '+address+' 0:'+sensor+'|grep Processed|cut -b 21-25"')
  #stream = os.popen('ipmitool -H 192.168.0.2 -P "" -t '+address+' sensor|grep "'+sensor+'"|cut -b 20-25')
  stream = os.popen('ipmitool -H 10.0.0.21 -P "" sensor|grep "'+sensor+'"|cut -b 20-25')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  #print(sensor+ " "+temp_cc.strip())
  if temp_cc.strip()=="na": 
    return "na"
  return float(temp_cc.strip())

internal_temp=readtemp("0x92","Internal temp.")
SM_Top_temp=readtemp("0x92","SM Top Temp")
SM_Bottom_temp=readtemp("0x92","SM Bottom Temp")
SM_Center_temp=readtemp("0x92","SM Center Temp")
ZP_CM_MCU_temp=readtemp("0x92","ZP CM MCU Temp")
ZP_CM_FPGA_temp=readtemp("0x92","ZP CM FPGA Temp")
ZP_CM_FF_temp=readtemp("0x92","ZP CM FF Temp")
ZP_CM_Reg_temp=readtemp("0x92","ZP CM Reg Temp")
CM_MCU_temp=readtemp("0x92","^CM MCU Temp")
CM_FPGA_VU_temp=readtemp("0x92","CM FPGA VU Temp")
CM_FPGA_KU_temp=readtemp("0x92","CM FPGA KU Temp")
CM_Max_FF_temp=readtemp("0x92","CM Max FF Temp")
CM_Max_Reg_temp=readtemp("0x92","CM Max Reg Temp")
PIM400KZ_temp=readtemp("0x92","PIM400KZ Temp")
PIM400KZ_current=readtemp("0x92","PIM400KZ Current")

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
if internal_temp!="na": dblist.append(["apollo05.temperatues.internal_temp", ( timestamp, internal_temp ) ])
if SM_Top_temp!="na": dblist.append(["apollo05.temperatues.SM_Top_temp", ( timestamp, SM_Top_temp ) ])
if SM_Bottom_temp!="na": dblist.append(["apollo05.temperatues.SM_Bottom_temp", ( timestamp, SM_Bottom_temp ) ])
if SM_Center_temp!="na": dblist.append(["apollo05.temperatues.SM_Center_temp", ( timestamp, SM_Center_temp ) ])
if ZP_CM_MCU_temp!="na": dblist.append(["apollo05.temperatues.ZP_CM_MCU_temp", ( timestamp, ZP_CM_MCU_temp ) ])
if ZP_CM_FPGA_temp!="na": dblist.append(["apollo05.temperatues.ZP_CM_FPGA_temp", ( timestamp, ZP_CM_FPGA_temp ) ])
if ZP_CM_FF_temp!="na": dblist.append(["apollo05.temperatues.ZP_CM_FF_temp", ( timestamp, ZP_CM_FF_temp ) ])
if ZP_CM_Reg_temp!="na": dblist.append(["apollo05.temperatues.ZP_CM_Reg_temp", ( timestamp, ZP_CM_Reg_temp ) ])
if CM_MCU_temp!="na": dblist.append(["apollo05.temperatues.CM_MCU_temp", ( timestamp, CM_MCU_temp) ])
if CM_FPGA_VU_temp!="na": dblist.append(["apollo05.temperatues.CM_FPGA_VU_temp", ( timestamp,CM_FPGA_VU_temp ) ])
if CM_FPGA_KU_temp!="na": dblist.append(["apollo05.temperatues.CM_FPGA_KU_temp", ( timestamp, CM_FPGA_KU_temp) ])
if CM_Max_FF_temp!="na": dblist.append(["apollo05.temperatues.CM_Max_FF_temp", ( timestamp,CM_Max_FF_temp ) ])
if CM_Max_Reg_temp!="na": dblist.append(["apollo05.temperatues.CM_Max_Reg_temp", ( timestamp, CM_Max_Reg_temp) ])
if PIM400KZ_temp!="na": dblist.append(["apollo05.temperatues.PIM400KZ_temp", ( timestamp, PIM400KZ_temp) ])
if PIM400KZ_current!="na": dblist.append(["apollo05.temperatues.PIM400KZ_current", ( timestamp, PIM400KZ_current) ])



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

