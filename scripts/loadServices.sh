#!/bin/bash
for i in `ls /dev/ttyUSB*`
  do 
  a=`udevadm info --query=all $i|grep "ID_VENDOR_ID=0590"`
   if [ $? -eq 0 ]
     then DEV=$i
   fi
done
/usr/bin/python3.4 /home/tkuser/OmronSensor.py  $DEV
