# Measurement Car Tracking System 

The system is based on [Traccar service](https://www.traccar.org/) runnig on the server. The data are uploaded from measurement cars from [Turris Omnia](https://www.turris.com/en/omnia/overview/) with [GNSS enabled LTE modem](https://doc.turris.cz/doc/cs/public/gps).

## Installation 

    opkg update 
    opkg install gpsd gpsd-clients jq

## Usage

    watch -n 30 position_upload.sh
