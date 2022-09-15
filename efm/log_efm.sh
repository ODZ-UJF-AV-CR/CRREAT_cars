#!/bin/bash
echo "THUNDERMILL01 data logger"
echo "To exit, pres ctrl-a, ctrl-x"
echo " "


# Set if not exists
STATION=${STATION:-'CAR1'}
CARDOS_USB=${CARDOS_USB:-'/dev/ttyUSB1'}


mkdir /data/cardos/ -p >/dev/null 2>&1
echo "Soupstim zaznam"
stty 115200 < ${CARDOS_USB}
sed -u '/^$/d' ${CARDOS_USB} | ts '%Y%m%d_%H%M%.S,' | tee /data/cardos/CARDOS_${STATION}_$(date +"%Y%m%d_%H%M%S").log
echo "Konec"
