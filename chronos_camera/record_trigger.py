#!/usr/bin/python3

import requests

#inspired by https://github.com/krontech/chronos-examples/tree/master/python3

post = requests.post('http://chronos.lan/control/startFilesave', json = {'format': 'h264', 'device': 'mmcblk1p1'})
print(post.reason)
