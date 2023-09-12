#!/usr/bin/python3

import socket
import pickle
import struct
import serial
import time
from datetime import datetime
import sys
import math
import snap7


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
client.connect('128.141.63.209', 0, 0)
topo = client.db_read(400,30,104)
topo2 = client.db_read(400,32,4)


#DB400.DBW30 etc ID 96 = RH (0 to 27648 counts translate to 0 to 100% RH, RH = ADC * 0.0036169)
#DB400.DBW40 etc ID 98 = T (0 to 27648 counts translate to 0 to 50 C, T = ADC * 0.00180845)
#DB400.DBW50 etc ID 100 = Flow (0 to 27648 counts SHOULD translate to 0 to 50 l/min, Flow = ADC * 0.00180845)
#DB400.DBW60 etc ID 102 = NC
#DB400.DBW70 etc ID 112 = RTD#1 Pt100 integer number of 0.1 Celsius (this is a 1200, remember!) T = ADC * 0.1
#DB400.DBW80 etc ID 114 = RTD#2 idem (disconnected?)
#DB400.DBW90 etc ID 116 = RTD#3 same as ID 112
#DB400.DBW100 etc ID 118 = RTD#4 same as ID 112

probes = {}
probes['ID_RH']=0
probes['RH']=2
probes['ID_T']=10
probes['T']=12
probes['Flow_ID']=20
probes['Flow']=22
probes['RTD1_ID']=40
probes['RTD1']=42
probes['RTD2_ID']=50
probes['RTD2']=52
probes['RTD3_ID']=60
probes['RTD3']=62
probes['RTD4_ID']=70
probes['RTD4']=72

temps={}

for probe in probes:
   byte_index=probes[probe]
   x = topo[byte_index:byte_index + 2]
   temps[probe] = struct.unpack('>h', struct.pack('2B', *x))[0]
   
#print("RH=",temps["RH"]*0.0036169," %")
#print("T=",temps["T"]*0.00180845," C")
#print("Flow=",temps["Flow"]*0.00180845," l/min")
#print("RTD1=",temps["RTD1"]*0.1," C")
#print("RTD2=",temps["RTD2"]*0.1," C")
#print("RTD3=",temps["RTD3"]*0.1," C")
#print("RTD4=",temps["RTD4"]*0.1," C")


try:
    timestamp = time.time()

    dblist = []
    dblist.append(["rackA16.sensors.rh", ( timestamp, temps["RH"]*0.0036169) ])
    dblist.append(["rackA16.sensors.t", ( timestamp, temps["T"]*0.00180845) ])
    dblist.append(["rackA16.sensors.flow", ( timestamp, temps["Flow"]*0.00180845) ])
    dblist.append(["rackA16.sensors.rtd1", ( timestamp, temps["RTD1"]*0.1) ])
    dblist.append(["rackA16.sensors.rtd2", ( timestamp, temps["RTD2"]*0.1) ])
    dblist.append(["rackA16.sensors.rtd3", ( timestamp, temps["RTD3"]*0.1) ])
    dblist.append(["rackA16.sensors.rtd4", ( timestamp, temps["RTD4"]*0.1) ])

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

except Exception as e:
  print(e)
  sys.exit()
