#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 13:38:11 2019

@author: wittich@cornell.edu 
"""


import time
import re
import pickle
import struct
import socket
from os import popen
from collections import defaultdict

# settable parameters
IPMI_IP = "192.168.38.125"
IPMI_ADDR = [ 0x5A, 0x5C, 0x8a, 0x94] # two fan trays and two apollo
IPMI_STR  = [ "FTL.", "FTU.", "AP05.","AP09."]
GRAPHITE_IP = '127.0.0.1'
GRAPHITE_PORT = 2004
carbon_directory = "atca.cornell."

#%%
def get_all_sensors(ipmi_ip, ipmi_addr):
    cmd = 'ipmitool -H %s -P "" -t 0x%x sensor ' % (ipmi_ip, ipmi_addr)
    print (cmd)
    output = popen(cmd).read()
    res = []
    for l in output.splitlines():
        s = l.split("|")
        sm = list(map(str.strip,s))
        res.append(sm)
        #print(",".join(sm))
    return res
    #print(s)

#%%
def map_fcn(val):
   if val == 'na' or val is None:
        return ""
   else:
        return str(val)
#%%
sleeptime=60.0


tempstr = re.compile("[Tt]em")
fanstr= re.compile("Tach")
db = ([])
ii = 0

# set up connection to Graphite database
sock = socket.socket()
sock.connect((GRAPHITE_IP, GRAPHITE_PORT))
starttime = time.time()
#%%
while True:
    sensors = defaultdict(list)
    for i in range(len(IPMI_ADDR)):
        sensor_raw = get_all_sensors(IPMI_IP, IPMI_ADDR[i])
        for s in sensor_raw:
            #print(s)
            s[0] = s[0].rstrip('\.')
            if tempstr.search(s[0]) or fanstr.search(s[0]) :
                sensors[IPMI_STR[i]+s[0]] = s[1]
    time_epoch= int(time.time())

    for key in sensors.keys():
        try:
            header = (carbon_directory + key).replace(" ", "_")
            val = float(sensors[key])
            db.append((header,(time_epoch, val)))
        except ValueError:
            print("can't make this a float:", sensors[key])

    if len(db) > 50 :
        payload = pickle.dumps(db, protocol=2)
        header = struct.pack("!L", len(payload))
        print(db)
        message = header + payload
        sock.sendall(message)
        ii = ii+ 1
        print('sent packet ', ii)
        db = ([])
    # sleep, taking into account how long the times took. 
    time.sleep(sleeptime- ((time.time()-starttime)%sleeptime))

sock.detach()
sock.close()

