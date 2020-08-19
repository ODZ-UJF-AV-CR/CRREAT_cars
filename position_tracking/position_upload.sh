#!/bin/sh
traccar=zoo.astro.cz/OsmAnd
port=80
id=CAR0

gpspipe=$( gpspipe -w |grep -m 1 TPV )
time=$( echo "$gpspipe" | jq -r '"\(.time)"')           # date/time in UTC
lat=$( echo "$gpspipe" | jq -r '"\(.lat)"')             # latitude
lon=$( echo "$gpspipe" | jq -r '"\(.lon)"')             # longitude
alt=$( echo "$gpspipe" | jq -r '"\(.alt)"')             # altitude (metres)
speed=$( echo "$gpspipe" | jq -r '"\(.speed)"')         # rate of movement (metres/sec)
hdop=$( gpspipe -w |grep -m 1 SKY |jq -r '"\(.hdop)"' ) # Dilution of Precision (meters)
curl -X POST http://$traccar:$port/?id=$id\&lat=$lat\&lon=$lon\&timestamp=$time\&altitude=$alt\&speed=$speed\&hdop=$hdop
