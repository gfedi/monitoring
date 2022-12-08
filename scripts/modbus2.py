from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('128.141.49.76')
#client = ModbusTcpClient('137.138.192.181')
client.write_coil(1, True)
result = client.read_coils(1,1)
print(result.bits[0])
client.close()
