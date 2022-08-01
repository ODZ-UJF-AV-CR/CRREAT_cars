#!/bin/bash
echo "GPSD data logger"
echo " "

STATION=${STATION:-'CARx'}

mkdir /data/gps/ -p >/dev/null 2>&1
echo "Soupstim zaznam"

gpspipe -R -P -w -o /data/gps/gps_${STATION}_$(date +"%Y%m%d_%H%M%S").log

echo "Konec"
