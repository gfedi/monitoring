#!/bin/bash

modprobe ftdi_sio
echo 0590 00d4 > /sys/bus/usb-serial/drivers/ftdi_sio/new_i

for i in `ls /dev/ttyUSB*`
  do 
  a=`udevadm info --query=all $i|grep "ID_VENDOR_ID=0590"`
   if [ $? -eq 0 ]
     then DEV=$i
   fi
done
/usr/bin/python3 /home/gfedi/monitoring/scripts/OmronSensor.py  $DEV
