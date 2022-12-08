import sys
import re
import time
import snap7
import struct
from ROOT import *
import colorsys
import os
import socket

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
  return float(temp_cc)

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


client = snap7.client.Client()
#client.connect('137.138.192.166', 0, 2)
client.connect('128.141.223.233', 0, 2)


sequence = ['X1FTop','X1FBottom','X1OFTop','X1OFBottom','X1ORTop','X1ORBottom','X0FTop','X0FBottom','X0OFTop','X0OFBottom','X0ORTop','X0ORBottom','X1HS1','X1HS2','X1HS3']

probes = {}
probes['X1FTop']=0
probes['X1ORBottom']=4
probes['X1HS3']=8
probes['X1ORTop']=16
probes['X1OFBottom']=20
probes['X1OFTop']=24
probes['X1FBottom']=28
probes['X0OFTop']=32
probes['X0FBottom']=36
probes['X1HS1']=40
probes['X1HS2']=44
probes['X0ORBottom']=48
probes['X0FTop']=52
probes['X0OFBottom']=56
probes['X0ORTop']=60

#34: X1FTop
#38: X1ORBottom
#42: non connesso (e si vede!)
#46: non connesso (e si vede!)
#50: X1ORTop
#54: X1OFBottom
#58: X1OFTop
#62: X1FBottom
#66: X0OFTop
#70: X0FBottom
#74: non connesso (e si vede!)
#78: non connesso (e si vede!)
#82: X0ORBottom
#86: X0FTop
#90: X0OFBottom
#94: X0ORTop

#for i in range(16):
#  byte_index=4*i
#  x = topo[byte_index:byte_index + 4]
#  real = struct.unpack('>f', struct.pack('4B', *x))[0]
#  print real

temps = {}

img = TImage.Open("board.png")

img.SetConstRatio(0)
img.SetImageQuality(TAttImage.kImgBest)

img.Draw()
c = gROOT.GetListOfCanvases().FindObject("boardpng")
c.SetWindowSize(800, 1000)

trange=(20.,100.)
trange_opt=(20.,50.)

raw_in=""

deg = u"\u00b0"

while raw_in.strip() != 'e':

	topo = client.db_read(1,34,64)
 
        #for ii in range(16):
	#  x = topo[ii*4:ii*4 + 4]
	#  print ii,struct.unpack('>f', struct.pack('4B', *x))[0]
          
	for probe in probes:
	  byte_index=probes[probe]
	  x = topo[byte_index:byte_index + 4]
	  temps[probe] = struct.unpack('>f', struct.pack('4B', *x))[0]

	for probe in sequence:
	  print probe, "={:0.2f}".format(temps[probe])

	#print rangeconv(trange,30.)

	img4 = img.Clone("img4")
	img4.Merge(img4, "allanon")
	X1FTop_rgb=colorsys.hls_to_rgb(float(rangeconv(trange,temps['X1FTop']))/255.,0.5,1.0)
	X1FBottom_rgb=colorsys.hls_to_rgb(float(rangeconv(trange,temps['X1FBottom']))/255.,0.5,1.0)
	X0FTop_rgb=colorsys.hls_to_rgb(float(rangeconv(trange,temps['X0FTop']))/255.,0.5,1.0)
	X0FBottom_rgb=colorsys.hls_to_rgb(float(rangeconv(trange,temps['X0FBottom']))/255.,0.5,1.0)
	X1ORTop_rgb=colorsys.hls_to_rgb(float(rangeconv(trange_opt,temps['X1ORTop']))/255.,0.5,1.0)
	X1ORBottom_rgb=colorsys.hls_to_rgb(float(rangeconv(trange_opt,temps['X1ORBottom']))/255.,0.5,1.0)
	X1OFTop_rgb=colorsys.hls_to_rgb(float(rangeconv(trange_opt,temps['X1OFTop']))/255.,0.5,1.0)
	X1OFBottom_rgb=colorsys.hls_to_rgb(float(rangeconv(trange_opt,temps['X1OFBottom']))/255.,0.5,1.0)
	X0OFTop_rgb=colorsys.hls_to_rgb(float(rangeconv(trange_opt,temps['X0OFTop']))/255.,0.5,1.0)
	X0OFBottom_rgb=colorsys.hls_to_rgb(float(rangeconv(trange_opt,temps['X0OFBottom']))/255.,0.5,1.0)
	X0ORTop_rgb=colorsys.hls_to_rgb(float(rangeconv(trange_opt,temps['X0ORTop']))/255.,0.5,1.0)
	X0ORBottom_rgb=colorsys.hls_to_rgb(float(rangeconv(trange_opt,temps['X0ORBottom']))/255.,0.5,1.0)
	X1F="#"+"%0.2x"%(int(X1FTop_rgb[0]*255))+"%0.2x"%(int(X1FTop_rgb[1]*255))+"%0.2x"%(int(X1FTop_rgb[2]*255))+" #"+"%0.2x"%(int(X1FBottom_rgb[0]*255))+"%0.2x"%(int(X1FBottom_rgb[1]*255))+"%0.2x"%(int(X1FBottom_rgb[2]*255))
	X0F="#"+"%0.2x"%(int(X0FTop_rgb[0]*255))+"%0.2x"%(int(X0FTop_rgb[1]*255))+"%0.2x"%(int(X0FTop_rgb[2]*255))+" #"+"%0.2x"%(int(X0FBottom_rgb[0]*255))+"%0.2x"%(int(X0FBottom_rgb[1]*255))+"%0.2x"%(int(X0FBottom_rgb[2]*255))
	X1OR="#"+"%0.2x"%(int(X1ORTop_rgb[0]*255))+"%0.2x"%(int(X1ORTop_rgb[1]*255))+"%0.2x"%(int(X1ORTop_rgb[2]*255))+" #"+"%0.2x"%(int(X1ORBottom_rgb[0]*255))+"%0.2x"%(int(X1ORBottom_rgb[1]*255))+"%0.2x"%(int(X1ORBottom_rgb[2]*255))
	X1OF="#"+"%0.2x"%(int(X1OFTop_rgb[0]*255))+"%0.2x"%(int(X1OFTop_rgb[1]*255))+"%0.2x"%(int(X1OFTop_rgb[2]*255))+" #"+"%0.2x"%(int(X1OFBottom_rgb[0]*255))+"%0.2x"%(int(X1OFBottom_rgb[1]*255))+"%0.2x"%(int(X1OFBottom_rgb[2]*255))
	X0OF="#"+"%0.2x"%(int(X0OFTop_rgb[0]*255))+"%0.2x"%(int(X0OFTop_rgb[1]*255))+"%0.2x"%(int(X0OFTop_rgb[2]*255))+" #"+"%0.2x"%(int(X0OFBottom_rgb[0]*255))+"%0.2x"%(int(X0OFBottom_rgb[1]*255))+"%0.2x"%(int(X0OFBottom_rgb[2]*255))
	X0OR="#"+"%0.2x"%(int(X0ORTop_rgb[0]*255))+"%0.2x"%(int(X0ORTop_rgb[1]*255))+"%0.2x"%(int(X0ORTop_rgb[2]*255))+" #"+"%0.2x"%(int(X0ORBottom_rgb[0]*255))+"%0.2x"%(int(X0ORBottom_rgb[1]*255))+"%0.2x"%(int(X0ORBottom_rgb[2]*255))
	img4.Gradient(90, X1F, "0 1" , 375, 325, 170, 170) #X1F
	img4.Gradient(90, X0F, "0 1", 375, 960, 170, 170) #X0F
	img4.Gradient(90, X1OF, "0 1", 210, 250, 35, 330) 
	img4.Gradient(90, X1OR, "0 1", 680, 250, 35, 330)
	img4.Gradient(90, X0OF, "0 1", 210, 885, 35, 330)
	img4.Gradient(90, X0OR, "0 1", 680, 885, 35, 330)
	for k in range(int(trange[0]),int(trange[1])):
	 rgb=colorsys.hls_to_rgb(float(rangeconv(trange,k))/255.,0.5,1.0)
	 img4.FillRectangle("#"+"%0.2x"%(int(rgb[0]*255))+"%0.2x"%(int(rgb[1]*255))+"%0.2x"%(int(rgb[2]*255)), 20+(100-rangeconv(trange,k))*6,1300, int(trange[1]-trange[0]/100*6), 50)
	textc1=TText(.01,.95,str(trange[0])+" \xB0"+"C")
	textc2=TText(.01,.95,str(trange[1])+" \xB0"+"C")
	textfpga=TText(.01,.95,"FPGAs")
	img4.DrawText(textc1,20,1400)
	img4.DrawText(textc2,20+100*6,1400)
	img4.DrawText(textfpga,10+50*6,1340)
	for k in range(int(trange_opt[0]),int(trange_opt[1])):
	 rgb=colorsys.hls_to_rgb(float(rangeconv(trange_opt,k))/255.,0.5,1.0)
	 img4.FillRectangle("#"+"%0.2x"%(int(rgb[0]*255))+"%0.2x"%(int(rgb[1]*255))+"%0.2x"%(int(rgb[2]*255)), 20+(100-rangeconv(trange_opt,k))*6,50, int(trange_opt[1]-trange_opt[0]/100*6), 50)
	textc1_opt=TText(.01,.95,str(trange_opt[0])+" \xB0"+"C")
	textc2_opt=TText(.01,.95,str(trange_opt[1])+" \xB0"+"C")
	textopt=TText(.01,.95,"Optics")
	img4.DrawText(textc1_opt,20,150)
	img4.DrawText(textc2_opt,20+100*6,150)
	img4.DrawText(textopt,10+50*6,90)
	img4.Draw()
	#text=TText(.70,.80,"Hello World!")
	#text.SetTextSize(40)
	#text.Draw("same")
	if len(sys.argv)>1:
	  textarg=TText(.01,.95, sys.argv[1])
	else:  
	  textarg=TText(.01,.95, "")


	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("192.168.0.103", 9221))
	sh1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sh1.connect(("192.168.0.102", 9221))
	sh2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sh2.connect(("192.168.0.101", 9221))

	img4.Draw()
	#text=TText(.70,.80,"Hello World!")
	#text.SetTextSize(40)
	#text.Draw("same")
	if len(sys.argv)>1:
	  textarg=TText(.01,.95, sys.argv[1])
	else:  
	  textarg=TText(.01,.95, "")


	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("192.168.0.103", 9221))
	sh1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sh1.connect(("192.168.0.102", 9221))
	sh2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sh2.connect(("192.168.0.101", 9221))

	s.sendall("V1?")
	VFPGA=float(s.recv(1024).split()[1])
	s.sendall("I1O?")
	IFPGA=float(re.sub('A','',s.recv(1024)))
	textpsu1=TText(.01,.95, "FPGA heaters "+"{:0.1f}".format(VFPGA)+"V "+"{:0.1f}".format(VFPGA*IFPGA)+"W")

	s.sendall("V2?")
	VOPT=float(s.recv(1024).split()[1])
	s.sendall("I2O?")
	IOPT=float(re.sub('A','',s.recv(1024)))
	textpsu2=TText(.01,.95, "OPTO heaters "+"{:0.1f}".format(VOPT)+"V "+"{:0.1f}".format(VOPT*IOPT)+"W")


        sh1.sendall("V1?")
        VFPGA_h1=float(sh1.recv(1024).split()[1])
        sh1.sendall("I1O?")
        IFPGA_h1=float(re.sub('A','',sh1.recv(1024)))
        sh1.sendall("V2?")
        VOPT_h1=float(sh1.recv(1024).split()[1])
        sh1.sendall("I2O?")
        IOPT_h1=float(re.sub('A','',sh1.recv(1024)))
        textpsu_h1=TText(.01,.95, "Heater-board L pow "+"{:0.1f}".format(VOPT_h1*IOPT_h1+VFPGA_h1*IFPGA_h1)+"W")

        sh2.sendall("V1?")
        VFPGA_h2=float(sh2.recv(1024).split()[1])
        sh2.sendall("I1O?")
        IFPGA_h2=float(re.sub('A','',sh2.recv(1024)))
        sh2.sendall("V2?")
        VOPT_h2=float(sh2.recv(1024).split()[1])
        sh2.sendall("I2O?")
        IOPT_h2=float(re.sub('A','',sh2.recv(1024)))
        textpsu_h2=TText(.01,.95, "Heater-board R pow "+"{:0.1f}".format(VOPT_h2*IOPT_h2+VFPGA_h2*IFPGA_h2)+"W")

        s.close()
        sh1.close()
        sh2.close()

	textexa1=TText(.01,.95, "T. in lower fans L="+str(readtemp("5a","7"))+" \xB0"+"C")
	textexa2=TText(.01,.95, "T. in lower fans C="+str(readtemp("5a","8"))+" \xB0"+"C")
	textexa3=TText(.01,.95, "T. in lower fans R="+str(readtemp("5a","9"))+" \xB0"+"C")
	textexa4=TText(.01,.95, "T. out upper fans L="+str(readtemp("5c","6"))+" \xB0"+"C")
	textexa5=TText(.01,.95, "T. out upper fans C="+str(readtemp("5c","7"))+" \xB0"+"C")
	textexa6=TText(.01,.95, "T. out upper fans R="+str(readtemp("5c","8"))+" \xB0"+"C")
	textrpm3=TText(.01,.95, "RPM lower fans="+str(readrpm("5a")))
	textrpm4=TText(.01,.95, "RPM upper fans="+str(readrpm("5c")))
	textexttemp=TText(.01,.95, "External temp ="+str(readexttemp())+" \xB0"+"C")


	img4.DrawText(textarg,750,40)
	img4.DrawText(textpsu1,750,80)
	img4.DrawText(textpsu2,750,120)
	img4.DrawText(textexa1,750,160)
	img4.DrawText(textexa2,750,200)
	img4.DrawText(textexa3,750,240)
	img4.DrawText(textexa4,750,280)
	img4.DrawText(textexa5,750,320)
	img4.DrawText(textexa6,750,360)
	img4.DrawText(textrpm3,750,400)
	img4.DrawText(textrpm4,750,440)
	img4.DrawText(textpsu_h1,750,480)
	img4.DrawText(textpsu_h2,750,520)
	img4.DrawText(textexttemp,750,560)

	#sequence = ['X1FTop','X1FBottom','X1OFTop','X1OFBottom','X1ORTop','X1ORBottom','X0FTop','X0FBottom','X0OFTop','X0OFBottom','X0ORTop','X0ORBottom']
	textX1HS1=TText(.01,.95, "{:0.1f}".format(temps['X1HS1'])+"\xB0"+"C")
	#img4.DrawText(textX1HS1,500,200)
	textX1HS2=TText(.01,.95, "{:0.1f}".format(temps['X1HS2'])+"\xB0"+"C")
	#img4.DrawText(textX1HS2,630,200)
	textX1HS3=TText(.01,.95, "{:0.1f}".format(temps['X1HS3'])+"\xB0"+"C")
	#img4.DrawText(textX1HS3,300,200)
	textX1FTop=TText(.01,.95, "{:0.1f}".format(temps['X1FTop'])+"\xB0"+"C")
	textX1FBottom=TText(.01,.95, "{:0.1f}".format(temps['X1FBottom'])+"\xB0"+"C")
	img4.DrawText(textX1FTop,405,320)
	img4.DrawText(textX1FBottom,405,530)
	textX0FTop=TText(.01,.95, "{:0.1f}".format(temps['X0FTop'])+"\xB0"+"C")
	textX0FBottom=TText(.01,.95, "{:0.1f}".format(temps['X0FBottom'])+"\xB0"+"C")
	img4.DrawText(textX0FTop,405,955)
	img4.DrawText(textX0FBottom,405,1165)
	textX1OFTop=TText(.01,.95, "{:0.1f}".format(temps['X1OFTop'])+"\xB0"+"C")
	textX1OFBottom=TText(.01,.95, "{:0.1f}".format(temps['X1OFBottom'])+"\xB0"+"C")
	img4.DrawText(textX1OFTop,210, 245)
	img4.DrawText(textX1OFBottom,210, 610)
	textX1ORTop=TText(.01,.95, "{:0.1f}".format(temps['X1ORTop'])+"\xB0"+"C")
	textX1ORBottom=TText(.01,.95, "{:0.1f}".format(temps['X1ORBottom'])+"\xB0"+"C")
	img4.DrawText(textX1ORTop,640, 245)
	img4.DrawText(textX1ORBottom,640, 610)
	textX0OFTop=TText(.01,.95, "{:0.1f}".format(temps['X0OFTop'])+"\xB0"+"C")
	textX0OFBottom=TText(.01,.95, "{:0.1f}".format(temps['X0OFBottom'])+"\xB0"+"C")
	img4.DrawText(textX0OFTop,210, 880)
	img4.DrawText(textX0OFBottom,210, 1245)
	textX0ORTop=TText(.01,.95, "{:0.1f}".format(temps['X0ORTop'])+"\xB0"+"C")
	textX0ORBottom=TText(.01,.95, "{:0.1f}".format(temps['X0ORBottom'])+"\xB0"+"C")
	img4.DrawText(textX0ORTop,640, 880)
	img4.DrawText(textX0ORBottom,640, 1245)

        c.Update()

	raw_in=raw_input("Press enter to continue, [e] to exit, [s] to save...")

        if raw_in.strip() == 's':
          c.SaveAs("temp.png")
	  os.system("convert -trim temp.png "+str(time.time())+".png")
	  os.system("rm temp.png")

        img4.Draw()
