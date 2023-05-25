#!/usr/bin/python3.6

from urllib.request import urlopen  
import json
import pandas as pd
import datetime

import socket
import pickle
import struct
import time

url = "https://api.open-meteo.com/v1/forecast?latitude=46.2330&longitude=6.0557&current_weather=true&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,cloudcover,precipitation"

response = urlopen(url)
  
data_json = json.loads(response.read())
  
current = data_json["current_weather"]
forecast = data_json["hourly"]

df = pd.DataFrame()

#print(data_json)

for i in forecast:
    #print(i)
    df[i]=forecast[i]

df["time"] = pd.to_datetime(df['time'])
delay = pd.Timestamp(current["time"])+pd.Timedelta(hours=24)
#print(df[df["time"]==delay])

#time
#temperature_2m
#relativehumidity_2m
#dewpoint_2m
#cloudcover
#precipitation
#                  time  temperature_2m  relativehumidity_2m  dewpoint_2m  cloudcover  precipitation
#40 2023-05-26 16:00:00            23.9                   48         12.3          46            0.0

timestamp = time.time()

dblist = []
dblist.append(["rackA16.weather.cern_temp", ( timestamp, float(current["temperature"])) ])
dblist.append(["rackA16.weather.cern_weathercode", ( timestamp, float(current["weathercode"])) ])
dblist.append(["rackA16.weather.fore_cloudcover", ( timestamp, float(df[df["time"]==delay]["cloudcover"].values[0])) ])
dblist.append(["rackA16.weather.fore_dewpoint", ( timestamp, float(df[df["time"]==delay]["dewpoint_2m"].values[0])) ])
dblist.append(["rackA16.weather.fore_humidity", ( timestamp, float(df[df["time"]==delay]["relativehumidity_2m"].values[0])) ])
dblist.append(["rackA16.weather.fore_precipitation", ( timestamp, float(df[df["time"]==delay]["precipitation"].values[0])) ])
dblist.append(["rackA16.weather.fore_temperature", ( timestamp, float(df[df["time"]==delay]["temperature_2m"].values[0])) ])


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
