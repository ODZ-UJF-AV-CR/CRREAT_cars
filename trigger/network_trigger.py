from socket import *
import socket
from struct import *
import struct
import sys
from datetime import datetime
import time

from twisted.internet import reactor
from sysfs.gpio import Controller, OUTPUT, INPUT, RISING, FALLING

CAR_NUMBER = 8

def pin_ctrl(p, state):
    #if pin.direction == 'out':
    #    print("IGNORUJI TO .. je to muj trigger")
    #else:
    print("TRIGGER JE ZMACKNUT", datetime.utcnow())
    print(send_timestamp(soc_gpio))


Controller.available_pins = [51, 56]
pin = Controller.alloc_pin(56, INPUT, pin_ctrl, FALLING)
pin_out = Controller.alloc_pin(51, OUTPUT)
time.sleep(0.1)
pin_out.set()

midnight = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

def send_timestamp(soc):
    time = datetime.utcnow()-midnight
    ms = int(round(time.total_seconds()*1000))
    print(ms)
    checksum = 0
    header = struct.pack(
        "!BBHHHLLL", 13, CAR_NUMBER, checksum, 255, 0, ms, 0, 0)
    print(header)

    soc.sendto(header, ("192.168.1.255", 0))


def ethernet_head(raw_data):
    print("RAW")
    r = raw_data
    print([b for b in raw_data])
    print("IPs {}.{}.{}.{}, IPd {}.{}.{}.{}".format(*r[12:20]))
    print("TYPE", raw_data[20])
    print("CODE", raw_data[21])
    print("Identifier", raw_data[23], raw_data[24])
    print("Sequence", raw_data[25], raw_data[26])
    print("Header", [b for b in raw_data[20:28]] )

    return raw_data


def icmp_thread():
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    #raw, addr = s.recvfrom(65565)
    #raw = ethernet_head(raw)
    while True:
        raw, addr = s.recvfrom(65565)
        print("ICMP type", raw[20], raw[21])
        if (raw[20] == 13 and raw[15] == 0 and raw[21] != CAR_NUMBER) or raw[20] == 8:
            #print([b for b in raw])

            #pin.direction = OUTPUT
            print("Vytvor trigger do detektoru")
            pin_out.reset()
            time.sleep(0.1)
            pin_out.set()
            #pin.direction = INPUT
            print("Ukonci trigger")

def gpio_thread():
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        port = gpio.wait_for_edge(GPIO_IN, gpio.RISING)
        send_timestamp(s)



reactor.callInThread(icmp_thread)
#it = threading.Thread(target=icmp_thread, args=None, daemon=True)

soc_gpio = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
soc_gpio.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
send_timestamp(soc_gpio)


#def pin_ctrl(p, state):
#    if pin.direction == 'out':
#        print("IGNORUJI TO .. je to muj trigger")
#    else:
#        print("TRIGGER JE ZMACKNUT", datetime.utcnow())
#        print(send_timestamp(soc_gpio))

reactor.run()
