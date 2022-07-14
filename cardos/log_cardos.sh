#!/bin/bash
echo "CARDOS01 data logger"
echo "To exit, pres ctrl-a, ctrl-x"
echo " "

mkdir /data/cardos/ -p >/dev/null 2>&1
echo "Soupstim zaznam"
stty 115200 < /dev/ttyUSB0
cat /dev/ttyUSB0 | ts '%Y%m%d_%H%M%.S,' | tee /data/cardos/CARDOS_$(date +"%Y%m%d_%H%M%S").log
#picocom -b 115200 -q /dev/ttyUSB0 | ts '%Y%m%d_%H%M%.S,' | tee /data/cardos/CARDOS_$(date +"%Y%m%d_%H%M%S").log
echo "Konec"
