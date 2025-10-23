# All-sky Lightning video capture system  

The system expect the Chronos high-speed camera mounted on car roof. The camera should be connected to 1Gigabit Ethernet and powered from stable power source.
The Recording mode should be activated manually from the camera web GUI.

## Example videos

### Daytime thunderstorm

[![Lightning capture demonstration video](https://img.youtube.com/vi/zzwEuAdUSWs/0.jpg)](https://youtu.be/zzwEuAdUSWs?t=18)
[![Lightning capture demonstration video](https://img.youtube.com/vi/TS5qrMavIaQ/0.jpg)](https://youtu.be/TS5qrMavIaQ?t=18)

### Nigth thunderstorm 

[![Lightning capture demonstration video](https://img.youtube.com/vi/mmvze8V5GRg/0.jpg)](https://youtu.be/mmvze8V5GRg?t=2)

## Installation

### Software

    sudo apt-get install python-requests


### Hardware

[Chronos 1.4 camera CR14-1.0-16M](https://www.krontech.ca/product/chronos-1-4-high-speed-camera) is mounted in waterproof [SolidBox 69200](https://www.elima.cz/obchod/68200-krabice-solidbox-ip65-270x220x126mm-plne-viko-hladke-boky-famatel-p-34205.html). The box is covered by plexiglass dome ~~[Duradom 200mm](https://www.amazon.com/CATLAB-Acrylic-Flange-Plastic-Hemisphere/dp/B07DNVWRHP)~~[Dahua SD50 bubble](https://www.asm.cz/cs/228337-dahua-bublina-kopule-plexi-pro-ptz-kamery-rady-sd50-napr-sd50230u).

![High-speed whole sky camera - Waterproof box with camera mount](doc/img/camera_mount.jpg)

The camera itself has wide angle CS [FE185C057HA-1](https://www.bhphotovideo.com/c/product/404281-REG/Fujinon_FE185C057HA1_FE185C057HA_1_2_3_1_8mm_F_1_4.html) lenses. The power of the camera is delivered from a 12V car on-board socket. The camera requires 20V as power input. Therefore the power voltage is converted by [power supply converter](https://www.alza.cz/EN/auto/oem-power-supply-converter-for-laptops-12-30v-90w-d6269710.htm),

The camera power is controlled by [car_power_controler](https://github.com/ODZ-UJF-AV-CR/car_power_controler).

## Usage

The camera should be in a "Recording" state. Then a call of the script causes a save of the video Recorded in  RAM.

    ./record_trigger.py


![Saving the video captured by Chronos high-speed camera](doc/img/saving_video.png)


This script disables the camera LCD to save power and then saves the recorded video from RAM.

I this case the LCD needs to be activated again. It could be done by a different script

    ./reenable_LCD.py


## Camera software 



### Enable SSHFS

SSHFS support is not enabled in the firmware that supplies KRONTECH, this can be eneabled easily by modifying the OpenSSH server configuration.

The following line needs to be added to the **beginning** of the file `/etc/ssh/sshd_config`. It is very important to place this text at the beginning of the file before the next configuration.

```
Subsystem sftp /usr/lib/openssh/sftp-server
```

The configuration can be validated by restarting the sshd server
```
service sshd restart
```



## Data processing 

Batch conversion of .raw files to directory with TIFFs:
```
for f in *.raw; do ~/convert_raw12.sh $f & done
```



Skript pro prevod slozek s TIFFy na MP4: 

```
for f in */; do ffmpeg -i ${f}_%06d.tiff -crf 0 ${f::-1}.mp4; done
```

```
for f in */; do ffmpeg -i ${f}_%06d.tiff -nostdin -loglevel panic -crf 0 ${f::-1}.mp4& done
```
