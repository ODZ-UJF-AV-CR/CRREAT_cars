#!/bin/bash
echo "CARDOS01 data logger"
echo "To exit, pres ctrl-a, ctrl-x"
echo "Waiting for time sync.. "
chronyc -h 192.168.1.2,::1 waitsync 0 0.1 0.0 1
echo "Time synchronized"


# Set if not exists
STATION=${STATION:-'CARx'}
CARDOS_USB=${CARDOS_USB:-'/dev/ttyUSB0'}


mkdir /data/cardos/ -p >/dev/null 2>&1
echo "Soupstim zaznam"
stty 115200 < ${CARDOS_USB}
sed -u '/^$/d' ${CARDOS_USB} | ts '%Y%m%d_%H%M%.S,' | tee /data/cardos/CARDOS_${STATION}_$(date +"%Y%m%d_%H%M%S").log
echo "Konec"
