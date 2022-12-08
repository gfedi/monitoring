import socket
import os
import subprocess
import time

def readtemp(address):
  stream = os.popen('ssh root@192.168.0.171 "clia sensordata '+address+' 0:4|grep Processed|cut -b 21-25"')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  return float(temp_cc)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.103", 9221))


sh1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sh1.connect(("192.168.0.102", 9221))

sh2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sh2.connect(("192.168.0.101", 9221))

s.sendall("V1 60.0")
s.sendall("V2 52.0")
#s.sendall("V2 36.58")
sh1.sendall("V1 10.0")
sh2.sendall("V1 10.0")
time.sleep(1)

s.sendall("OPALL 0")
#s.sendall("OP1 0")
sh1.sendall("OPALL 0")
sh2.sendall("OPALL 0")
time.sleep(1)

#print "Exhaust temp on 0xcc=",readtemp("0xcc")
#print "Exhaust temp on 0xc8=",readtemp("0xc8")
#print "Exhaust temp on 0xca=",readtemp("0xca")
#print "Exhaust temp on 0xce=",readtemp("0xce")


s.sendall("V1?")
print "Set voltage on mockup board, FPGA heaters=",s.recv(1024).split()[1]
#s.sendall("I1?")
#print s.recv(1024)
s.sendall("I1O?")
print "Measured current on mockup, FPGA heaters=",s.recv(1024)
s.sendall("V2?")
print "Set voltage on mockup board, OPTO heaters=",s.recv(1024).split()[1]
#s.sendall("I2?")
#print s.recv(1024)
s.sendall("I2O?")
print "Measured current on mockup board, OPTO heaters=",s.recv(1024)
#print s.recv(1024)


sh1.sendall("V1?")
print "Set voltage on heater board 1, FPGA heaters=",sh1.recv(1024).split()[1]
sh1.sendall("I1O?")
print "Measured current on heater board 1, FPGA heaters=",sh1.recv(1024)
sh1.sendall("V2?")
print "Set voltage on heater board 1, OPTO heaters=",sh1.recv(1024).split()[1]
sh1.sendall("I2O?")
print "Measured current on heater board 1, OPTO heaters=",sh1.recv(1024)

sh2.sendall("V1?")
print "Set voltage on heater board 2, FPGA heaters=",sh2.recv(1024).split()[1]
sh2.sendall("I1O?")
print "Measured current on heater board 2, FPGA heaters=",sh2.recv(1024)
sh2.sendall("V2?")
print "Set voltage on heater board 2, OPTO heaters=",sh2.recv(1024).split()[1]
sh2.sendall("I2O?")
print "Measured current on heater board 2, OPTO heaters=",sh2.recv(1024)

sh1.close()
sh2.close()
s.close()
