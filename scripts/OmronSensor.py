#!/usr/bin/python3.4

import socket
import pickle
import struct
import serial
import time
from datetime import datetime
import sys
import math
import snap7

# LED display rule. Normal Off.
DISPLAY_RULE_NORMALLY_OFF = 0

# LED display rule. Normal On.
DISPLAY_RULE_NORMALLY_ON = 1

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

def calc_crc(buf, length):
    """
    CRC-16 calculation.
    """
    crc = 0xFFFF
    for i in range(length):
        crc = crc ^ buf[i]
        for i in range(8):
            carrayFlag = crc & 1
            crc = crc >> 1
            if (carrayFlag == 1):
                crc = crc ^ 0xA001
    crcH = crc >> 8
    crcL = crc & 0x00FF
    return (bytearray([crcL, crcH]))

# Serial.
#ser = serial.Serial("/dev/ttyUSB0", 115200, serial.EIGHTBITS, serial.PARITY_NONE)
ser = serial.Serial( sys.argv[1], 115200, serial.EIGHTBITS, serial.PARITY_NONE)

try:
  # LED On. Color of Green.
  time.sleep(1)
  command = bytearray([0x52, 0x42, 0x0a, 0x00, 0x02, 0x11, 0x51, DISPLAY_RULE_NORMALLY_ON, 0x00, 0, 255, 0])
  command = command + calc_crc(command, len(command))
  ser.write(command)
  time.sleep(0.3)
  ret = ser.read(ser.inWaiting())

  while ser.isOpen():
   # Get Latest data Long.
    command = bytearray([0x52, 0x42, 0x05, 0x00, 0x01, 0x21, 0x50])
    command = command + calc_crc(command, len(command))
    tmp = ser.write(command)
    time.sleep(0.3)
    data = ser.read(ser.inWaiting())
  #print(data)
    
    client = snap7.client.Client()
    client.connect('128.141.63.209', 0, 0)
    topo = client.db_read(444,10,16)
    topo2 = client.db_read(445,2,16)
    humy_1 = client.db_read(402,36,1)
    humy_2 = client.db_read(402,44,1)


    probes = {}
    probes['RelHumidity']=0
    probes['TempAir']=4
    probes['DewPoint']=8
    probes['DewPointError']=12

    probes2 = {}
    probes2['SetWaterTemp']=0
    probes2['InletWaterTemp']=4
    probes2['OutletWaterTemp']=8
    probes2['ValveOpening']=12



    temps={}
    temps2={}

    for probe in probes:
      byte_index=probes[probe]
      x = topo[byte_index:byte_index + 4]
      temps[probe] = struct.unpack('>f', struct.pack('4B', *x))[0]

    for probe in probes2:
      byte_index=probes2[probe]
      x = topo2[byte_index:byte_index + 4]
      temps2[probe] = struct.unpack('>f', struct.pack('4B', *x))[0]



    timestamp = time.time()
    temperature = str(int(hex(data[9]) + '{:02x}'.format(data[8], 'x'), 16) / 100)
    relative_humidity = str(int(hex(data[11]) + '{:02x}'.format(data[10], 'x'), 16) / 100)
    ambient_light = str(int(hex(data[13]) + '{:02x}'.format(data[12], 'x'), 16))
    barometric_pressure = str(int(hex(data[17]) + '{:02x}'.format(data[16], 'x')
                                  + '{:02x}'.format(data[15], 'x') + '{:02x}'.format(data[14], 'x'), 16) / 1000)
    sound_noise = str(int(hex(data[19]) + '{:02x}'.format(data[18], 'x'), 16) / 100)
    eTVOC = str(int(hex(data[21]) + '{:02x}'.format(data[20], 'x'), 16))
    eCO2 = str(int(hex(data[23]) + '{:02x}'.format(data[22], 'x'), 16))
    discomfort_index = str(int(hex(data[25]) + '{:02x}'.format(data[24], 'x'), 16) / 100)
    heat_stroke = str(int(hex(data[27]) + '{:02x}'.format(data[26], 'x'), 16) / 100)
    vibration_information = str(int(hex(data[28]), 16))
    si_value = str(int(hex(data[30]) + '{:02x}'.format(data[29], 'x'), 16) / 10)
    pga = str(int(hex(data[32]) + '{:02x}'.format(data[31], 'x'), 16) / 10)
    seismic_intensity = str(int(hex(data[34]) + '{:02x}'.format(data[33], 'x'), 16) / 1000)
    temperature_flag = str(int(hex(data[36]) + '{:02x}'.format(data[35], 'x'), 16))
    relative_humidity_flag = str(int(hex(data[38]) + '{:02x}'.format(data[37], 'x'), 16))
    ambient_light_flag = str(int(hex(data[40]) + '{:02x}'.format(data[39], 'x'), 16))
    barometric_pressure_flag = str(int(hex(data[42]) + '{:02x}'.format(data[41], 'x'), 16))
    sound_noise_flag = str(int(hex(data[44]) + '{:02x}'.format(data[43], 'x'), 16))
    etvoc_flag = str(int(hex(data[46]) + '{:02x}'.format(data[45], 'x'), 16))
    eco2_flag = str(int(hex(data[48]) + '{:02x}'.format(data[47], 'x'), 16))
    discomfort_index_flag = str(int(hex(data[50]) + '{:02x}'.format(data[49], 'x'), 16))
    heat_stroke_flag = str(int(hex(data[52]) + '{:02x}'.format(data[51], 'x'), 16))
    si_value_flag = str(int(hex(data[53]), 16))
    pga_flag = str(int(hex(data[54]), 16))
    seismic_intensity_flag = str(int(hex(data[55]), 16))
    dew_point= str(get_dew_point_c(float(temperature),float(relative_humidity)))

    dblist = []
    dblist.append(["rackA09.cooling.setwatertemp", ( timestamp, temps2['SetWaterTemp']) ])
    dblist.append(["rackA09.cooling.inletwatertemp", ( timestamp, temps2['InletWaterTemp']) ])
    dblist.append(["rackA09.cooling.inletwatertemp2hago", ( timestamp-7200, temps2['InletWaterTemp']) ])
    dblist.append(["rackA09.cooling.outletwatertemp", ( timestamp, temps2['OutletWaterTemp']) ])
    dblist.append(["rackA09.cooling.valveopening", ( timestamp, temps2['ValveOpening']) ])
    dblist.append(["rackA09.sensors.temperature", ( timestamp, temperature ) ])
    dblist.append(["rackA09.sensors.RH", ( timestamp, relative_humidity) ])
    dblist.append(["rackA09.sensors.light", ( timestamp, ambient_light) ])
    dblist.append(["rackA09.sensors.pressure", ( timestamp, barometric_pressure) ])
    dblist.append(["rackA09.sensors.noise", ( timestamp, sound_noise) ])
    dblist.append(["rackA09.sensors.etvoc", ( timestamp, eTVOC) ])
    dblist.append(["rackA09.sensors.co2", ( timestamp, eCO2) ])
    dblist.append(["rackA09.sensors.vibration", ( timestamp, vibration_information) ])
    dblist.append(["rackA09.sensors.SIvalue", ( timestamp, si_value) ])
    dblist.append(["rackA09.sensors.pga", ( timestamp, pga) ])
    dblist.append(["rackA09.sensors.seismic_intensity", ( timestamp, seismic_intensity) ])
    dblist.append(["rackA09.sensors.dew_point", ( timestamp, dew_point ) ])
    dblist.append(["rackA09.sensors.dew_point2hago", ( timestamp-7200, dew_point ) ])
    dblist.append(["rackA09.sensors.condensation_NC", ( timestamp, humy_1[0]&0b00001 ) ])
    dblist.append(["rackA09.sensors.condensation_NO", ( timestamp, humy_2[0]&0b00001 ) ])

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

    
    time.sleep(60)

except Exception as e:
  command = bytearray([0x52, 0x42, 0x0a, 0x00, 0x02, 0x11, 0x51, DISPLAY_RULE_NORMALLY_OFF, 0x00, 0, 0, 0])
  command = command + calc_crc(command, len(command))
  ser.write(command)
  print(e)
  sys.exit()
