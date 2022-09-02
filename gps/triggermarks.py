import socket
from pyubx2 import UBXReader


stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stream.connect(("192.168.1.1", 2947))
stream.send(b'?WATCH={"enable":true, "raw":2, "nmea": true, "json": false, "pps": true}\n')

print(stream)
file = stream.makefile('rb')
print(file)
#for x in file:
#    print(x)
#print(file)

ubr = UBXReader(file, protfilter=2)
for (raw_data, parsed_data) in ubr.iterate():
    #print(parsed_data)
    #print(".", end="", flush =1)
    #print(raw_data)
    #if "TIM" in parsed_data.identity:
    #    print(parsed_data)
    if parsed_data.identity in ["TIM-TM2"]:
    #    print(" ")
        print(parsed_data)
    #print(parsed_data.identity)

