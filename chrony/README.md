# Použití chrony v autech




# Omnia 
Omnia je centrálním zdrojem času v autech. Protože obsahuje relativně dobrý RTC obvod a zároveň je k ní převeden PPS signál z ublox GNSS příjímače. 




### Konfigurace

Soubor `/etc/chrony/chrony.conf`

```
# This file is included from config file generated from /etc/config/chrony

# Log clock errors above 0.5 seconds
# logchange 0.5

bindcmdaddress 0.0.0.0
cmdallow 192.168.1.0/24

# Don't log client accesses
noclientlog
allow 192.168.1.0/24
driftfile /srv/chrony/drift
makestep 1.0 3
leapsectz right/UTC
logdir /srv/chrony/log/

# set the system clock else the kernel will always stay in UNSYNC state
rtcsync

server SHM maxpoll 2

refclock SHM 0 poll 3 refid UBLX offset 0.2 noselect
refclock PPS /dev/pps0 lock UBLX refid PPS
```


# MOX

### Konfigurace

```
# Load UCI configuration
confdir /var/etc/chrony.d

logdir /srv/chrony
log measurements statistics tracking

# Load NTP servers from DHCP if enabled in UCI
# sourcedir /var/run/chrony-dhcp

server 192.168.1.1 iburst maxpoll 2 prefer

# Log clock errors above 0.5 seconds
logchange 0.5

# Don't log client accesses
noclientlog

# Mark the system clock as synchronized
rtcsync

#driftfile /srv/chrony/drift

ntsdumpdir /srv/chrony

```
