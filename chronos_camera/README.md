# Lightning video capture system  

The system expect the Chronos camera mounted on car roof. The camera should be connected to 1Gigabit ethernet and powered from stable power source.
The Recording mode should be activeted manually from the camera web GUI.

## Installation

    sudo apt-get install python-requests

## Usage

    ./record_trigger.py

This script disable camera LCD to save power and then save the recorded video from RAM.

I the case the LCD needs to be activated again. It could be done by different script

    ./reenable_LCD.py
