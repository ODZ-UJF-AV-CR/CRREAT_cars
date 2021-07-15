# Lightning video capture system  

The system expect the Chronos high-speed camera mounted on car roof. The camera should be connected to 1Gigabit ethernet and powered from stable power source.
The Recording mode should be activated manually from the camera web GUI.


## Installation

### Software

    sudo apt-get install python-requests


### Hardware

[Chronos 1.4 camera](https://www.krontech.ca/store/Chronos-1-4-High-Speed-Camera-p92268927) is mounted in waterproof [SolidBox 69200](https://www.elima.cz/obchod/68200-krabice-solidbox-ip65-270x220x126mm-plne-viko-hladke-boky-famatel-p-34205.html).

Camera itself has wide angle CS lenses.

![Waterproof box with camera mount](doc/img/camera_mount.jpg)

Power of the camera is delivered from 12V car on-board socket. The camera requires 20V as power input. Therefore the power voltage is converted by [power supply converter](https://www.alza.cz/EN/auto/oem-power-supply-converter-for-laptops-12-30v-90w-d6269710.htm)

## Usage

The camera should be in "Recording" state. Then a call of the script causes a save of the video Recorded in  RAM.

    ./record_trigger.py


![Saving the video captured by Chronos high-speed camera](doc/img/saving_video.png)


This script disable camera LCD to save power and then save the recorded video from RAM.

I the case the LCD needs to be activated again. It could be done by different script

    ./reenable_LCD.py
