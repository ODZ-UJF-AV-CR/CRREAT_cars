#!/bin/bash
echo "GPSD data logger"
echo " "

STATION=${STATION:-'CARx'}

mkdir /data/gps/ -p >/dev/null 2>&1
echo "Spoustim zaznam"

gpsd /dev/ttyACM0 /dev/ttyACM1 /dev/ttyACM2 -F /run/gpsd.sock &

sleep 3

gpspipe -R -P -w -o /data/gps/base_gps_${STATION}_$(date +"%Y%m%d_%H%M%S").log ::/dev/ttyACM0 &
gpspipe -R -P -w -o /data/gps/rover1_gps_${STATION}_$(date +"%Y%m%d_%H%M%S").log ::/dev/ttyACM1 &
gpspipe -R -P -w -o /data/gps/rover2_gps_${STATION}_$(date +"%Y%m%d_%H%M%S").log ::/dev/ttyACM2 

echo "Konec"
