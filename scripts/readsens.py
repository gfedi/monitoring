import os

def readtemp(address):
  stream = os.popen('ssh root@192.168.0.171 "clia sensordata '+address+' 0:4|grep Processed|cut -b 21-25"')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  return float(temp_cc)

print readtemp("0xca")
