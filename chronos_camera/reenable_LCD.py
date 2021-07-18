#!/usr/bin/python3

import requests
import time
from datetime import datetime

camera_url = "http://chronos.lan"

#inspired by https://github.com/krontech/chronos-examples/tree/master/python3

# disable camera backlight LCD to save power and reduce temperature
post = requests.post(camera_url+'/control/p', json = {'backlightEnabled': True })
if post.reason == "OK" :
	print("Camera LCD backlight sucesfully Enabled")
else:
    print(post)
