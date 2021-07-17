#!/usr/bin/python3

import requests
import time
from datetime import datetime

camera_url = "http://chronos.lan"

#inspired by https://github.com/krontech/chronos-examples/tree/master/python3

# disable camera backlight LCD to save power and reduce temperature
post = requests.post(camera_url+'/control/p', json = {'backlightEnabled': False })
if post.reason == "OK" :
	print("Camera LCD backlight sucesfully Disabled")
else:
    print(post)

post = requests.post(camera_url+'/control/stopRecording')
if post.reason == "OK":
    print("Recording stopped.")
else:
    print(post)

post = requests.post(camera_url+'/control/flushRecording')
if post.reason == "OK":
    print("Recording buffer flushed.")
else:
    print(post)

post = requests.post(camera_url+'/control/p', json = {'resolution': {'hRes': 928, 'vRes': 928, 'hOffset': 176, 'vOffset': 66}})
if post.reason == "OK":
    print("Video resolution is set.")
else:
    print(post)

post = requests.post(camera_url+'/control/p', json = {'recMaxFrames':4837})  # cca 3 s
if post.reason == "OK":
    print("Video Recording lenght is set.")
else:
    print(post)

post = requests.post(camera_url+'/control/p', json = {'recTrigDelay':2418})  # This value is only informative (it works for HW trigger only)
if post.reason == "OK":
    print("Text overlay is inicialized.")
else:
    print(post)

try:
	current_time = datetime.now()

	filename = current_time.strftime("%Y-%m-%d-%H-%M-%S.%f")+"-lightning"

	post = requests.get(camera_url+'/control/p/videoState')
	if post.json() != {'videoState':'filesave'}:

	    post = requests.get(camera_url+'/control/p/state')
	    if post.json() == {'state':'recording'}:
	        post = requests.post(camera_url+'/control/stopRecording')
	        print("Stopping camera recording")

	    elif post.json() == {'state':'idle'}:
	        print("Camera is already idle")

	    else:
	        print(post.json())

	    post = requests.post(camera_url+'/control/startFilesave', json = {'format': 'h264', 'device': 'mmcblk1p1', 'filename': filename })
	    if post.reason == "OK" :
	    	print("Saving the video")
	    else:
	        print("Unable to save the video")
	        print(post)
	else:
	    print("Camera is already saving the video. Do not disturb!")

except requests.exceptions.HTTPError as e:
    # Whoops it wasn't a 200
    print("Error: " + str(e))
