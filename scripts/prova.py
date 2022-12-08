import time
import os

def readboard(num):
  stream = os.popen('ssh root@192.168.0.2 "clia fru '+num+' 0"')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  return temp_cc

def getstatus(status):
  output = "OFF"
  for line in status:
     if line.find('Hot Swap State: M4') > 0:
       output = "ON"

  return output

boards ={}
boards['8a']=5
boards['82']=7
boards['84']=8
boards['8c']=10
boards['90']=11

for board in boards.keys():
  status = readboard(board).splitlines() 
  print(getstatus(status))
