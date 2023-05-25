#!/usr/bin/python

import datetime
import sys
import re
import time
import snap7
import struct
import colorsys
import os
import socket
import math

def get_dew_point_c(t_air_c, rel_humidity):
    """Compute the dew point in degrees Celsius
    :param t_air_c: current ambient temperature in degrees Celsius
    :type t_air_c: float
    :param rel_humidity: relative humidity in %
    :type rel_humidity: float
    :return: the dew point in degrees Celsius
    :rtype: float
    """
    A = 17.27
    B = 237.7
    alpha = ((A * t_air_c) / (B + t_air_c)) + math.log(rel_humidity/100.0)
    return (B * alpha) / (A - alpha)


client = snap7.client.Client()
#client.connect('172.26.223.107', 0, 0)
client.connect('128.141.63.209', 0, 0)


sequence = ['X1FTop','X1FBottom','X1OFTop','X1OFBottom','X1ORTop','X1ORBottom','X0FTop','X0FBottom','X0OFTop','X0OFBottom','X0ORTop','X0ORBottom']

probes = {}
probes['RelHumidity']=0
probes['TempAir']=4
probes['DewPoint']=8
probes['DewPointError']=12

probes2 = {}
probes2['SetWaterTemp']=0
probes2['InletWaterTemp']=4
probes2['OutletWaterTemp']=8
probes2['ValveOpening']=12



topo = client.db_read(444,10,16)
topo2 = client.db_read(445,2,16)
temps={}
temps2={}

for probe in probes:
  byte_index=probes[probe]
  x = topo[byte_index:byte_index + 4]
  temps[probe] = struct.unpack('>f', struct.pack('4B', *x))[0]


for probe in probes2:
  byte_index=probes2[probe]
  x = topo2[byte_index:byte_index + 4]
  temps2[probe] = struct.unpack('>f', struct.pack('4B', *x))[0]

#for probe in probes:
 # print probe, "={:0.2f}".format(temps[probe])

#for probe in probes2:
#  print probe, "={:0.2f}".format(temps2[probe])

#print("My dew point calculation",get_dew_point_c(temps['TempAir'],temps['RelHumidity']))

alert="OK"
if temps2['InletWaterTemp']-temps['DewPoint']<0: 
  alert="ALERT"
  print(alert)
elif temps2['InletWaterTemp']-temps['DewPoint']<1: 
  alert="WARNING"
  print(alert)


with open('dewalarm.log','a') as f:
   f.write(str(datetime.date.today())+" "+str(time.strftime("%H:%M:%S",time.localtime()))+", "+str(temps['RelHumidity'])+", "+str(temps['TempAir'])+", "+str("{:0.2f}".format(temps['DewPoint']))+", "+str("{:0.2f}".format(temps2['SetWaterTemp']))+", "+str("{:0.2f}".format(temps2['InletWaterTemp']))+", "+str("{:0.2f}".format(temps2['OutletWaterTemp']))+", "+str("{:0.2f}".format(temps2['ValveOpening']))+", "+alert+"\n")


if alert=="ALERT" or alert=="WARNING":
  subject="Subject: *** W A T C H  O U T *** TIF Rack dew point monitor, status: "+alert
  os.system("echo "+"\""+subject+"\""+">mail.tmp")
  os.system("echo 'Latest readings (one day)' >>mail.tmp") 
  os.system("echo 'Time, RH%, Air Temp, DewPoint, Cooling set temp, Cooling inlet temp, Cooling outlet temp, Valve opening, Status' >>mail.tmp") 
  os.system("cat dewalarm.log|tail -n 96 >>mail.tmp")
  os.system("/usr/sbin/sendmail 'giacomo.fedi@cern.ch,fabrizio.palla@cern.ch,Piero.Giorgio.Verdini@cern.ch' < mail.tmp")
  #os.system('echo `cat dewalarm.log|tail -n 96|sed '':a;N;$!ba;s/\n/\r\n/g''`|mail -s "TIF Rack dew point monitor, status: '+alert+'"  gfedi@cern.ch')
