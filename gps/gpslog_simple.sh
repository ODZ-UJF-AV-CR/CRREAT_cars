#!/bin/bash
echo "GPSD data logger"
echo " "

STATION=${STATION:-'CARx'}

mkdir /data/gps/ -p >/dev/null 2>&1
echo "Spoustim zaznam"

sleep 10
gpspipe -R -P -w -o /data/gps/omnia_gps_${STATION}_$(date +"%Y%m%d_%H%M%S").log 192.168.1.1 

echo "Konec"
