#!/usr/bin/python3

import requests

post = requests.post('http://chronos.lan/control/startFilesave', json = {'format': 'h264', 'device': 'mmcblk1p1'})
print(post.reason)
