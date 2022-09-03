import socket
from pyubx2 import UBXReader


stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stream.connect(("192.168.1.1", 2947))
stream.send(b'?WATCH={"enable":true, "raw":2, "nmea": true, "json": false, "pps": true}\n')

print(stream)
stream_file = stream.makefile('rb')
print(stream_file)
#for x in file:
#    print(x)
#print(file)
file_name="casove_znacky.csv"
file=open(file_name, "a")


ubr = UBXReader(stream_file, protfilter=2)
for (raw_data, parsed_data) in ubr.iterate():
    #print(parsed_data)
    #print(".", end="", flush =1)
    #print(raw_data)
    #if "TIM" in parsed_data.identity:
    #    print(parsed_data)
    if parsed_data.identity in ["TIM-TM2"]:
    #    print(" ")
        print(parsed_data)
        retezec=""
        retezec += str(parsed_data.ch)+","
        retezec += str(parsed_data.mode)+","
        retezec += str(parsed_data.run)+","
        retezec += str(parsed_data.newFallingEdge)+","
        retezec += str(parsed_data.timeBase)+","
        retezec += str(parsed_data.utc)+","
        retezec += str(parsed_data.time)+","
        retezec += str(parsed_data.newRisingEdge)+","
        retezec += str(parsed_data.count)+","
        retezec += str(parsed_data.wnR)+","
        retezec += str(parsed_data.wnF)+","
        retezec += str(parsed_data.towMsR)+","
        retezec += str(parsed_data.towSubMsR)+","
        retezec += str(parsed_data.towMsF)+","
        retezec += str(parsed_data.towSubMsF)+","
        retezec += str(parsed_data.accEst)+","


# UBX(TIM-TM2, ch=0, mode=1, run=0, newFallingEdge=1, timeBase=2, utc=1, time=1, newRisingEdge=1, count=167, wnR=2225, wnF=2225, towMsR=566930967, towSubMsR=128565, towMsF=566930967, towSubMsF=300502, accEst=1073)>
        file.write(retezec+"/n/r")

    #print(parsed_data.identity)


