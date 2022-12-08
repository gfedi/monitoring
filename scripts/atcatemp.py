#!/usr/bin/python

import sys
import re
import time
import snap7
import struct
import colorsys
import os
import socket
import datetime

def readtemp(address,sensor):
  stream = os.popen('ssh root@192.168.0.2 "clia sensordata '+address+' 0:'+sensor+'|grep Processed|cut -b 21-25"')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  return float(temp_cc)

def readrpm(address):
  stream = os.popen('ssh root@192.168.0.2 "clia sensordata '+address+' 0:10|grep Processed|cut -b 21-24"')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  return float(temp_cc.rstrip())

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



#print("T. in lower fans L="+str(readtemp("5a","7"))+" \xc2\xb0"+"C")
#print("T. in lower fans C="+str(readtemp("5a","8"))+" \xc2\xb0"+"C")
#print("T. in lower fans R="+str(readtemp("5a","9"))+" \xc2\xb0"+"C")
#print("T. out upper fans L="+str(readtemp("5c","6"))+" \xc2\xb0"+"C")
#print("T. out upper fans C="+str(readtemp("5c","7"))+" \xc2\xb0"+"C")
#print("T. out upper fans R="+str(readtemp("5c","8"))+" \xc2\xb0"+"C")
#print("RPM lower fans="+str(readrpm("5a")))
#print("RPM upper fans="+str(readrpm("5c")))
#print("External temp ="+str(readexttemp())+" \xc2\xb0"+"C")

lower_left=readtemp("5a","7")
lower_center=readtemp("5a","8")
lower_right=readtemp("5a","9")
upper_left=readtemp("5c","6")
upper_center=readtemp("5c","7")
upper_right=readtemp("5c","8")
external=readexttemp()



alert="OK"
if lower_left>40 or lower_center>40 or lower_right>40 or upper_left>40 or upper_center>40 or upper_right>40 or external>40:
  alert="ALERT"
  print(alert)
elif lower_left>35 or lower_center>35 or lower_right>35 or upper_left>35 or upper_center>35 or upper_right>35 or external>35:
  alert="WARNING"
  print(alert)


with open('tempalarm.log','a') as f:
   f.write(str(datetime.date.today())+" "+str(time.strftime("%H:%M:%S",time.localtime()))+", "+str(lower_left)+", "+str(lower_right)+", "+str(lower_right)+", "+str(upper_left)+", "+str(upper_center)+", "+str(upper_right)+", "+str(readrpm("5a"))+", "+str(readrpm("5c"))+", "+str(external)+", "+alert+"\n")


#if alert=="ALERT" or alert=="WARNING":
#  subject="Subject: *** W A T C H  O U T *** TIF ATCA temperature monitor, status: "+alert
#  os.system("echo "+"\""+subject+"\""+">mailtemp.tmp")
#  os.system("echo 'Latest readings (one day)' >>mailtemp.tmp")
#  os.system("echo 'Time, lower_left, lower_center, lower_right, upper_left, upper_center, upper_right, lower fantray RPM, upper fantray RPM, external temp, status' >>mailtemp.tmp")
#  os.system("cat tempalarm.log|tail -n 96 >>mailtemp.tmp")
#  os.system("/usr/sbin/sendmail 'giacomo.fedi@cern.ch,fabrizio.palla@cern.ch,mark.pesaresi01@imperial.ac.uk,gregory.iles@cern.ch' < mailtemp.tmp")
