import sys
import subprocess
import datetime
from datetime import datetime, timedelta
import struct
import socket
import time
import pickle

# send the prediction to graphite
epoch_time = datetime(1970, 1, 1)
timestamp =  datetime.today() + timedelta(hours=2) - epoch_time
dblist = []
dblist.append(["rackA16.sensors.dewprediction", ( timestamp.total_seconds(), 7.33) ])

print(dblist)

payload = pickle.dumps(dblist, protocol=2)
header = struct.pack("!L", len(payload))
message = header + payload

sock = socket.socket()
sock.settimeout(1)
sock.connect(('128.141.49.116', 2004))
sock.send(message)

sock.close()
