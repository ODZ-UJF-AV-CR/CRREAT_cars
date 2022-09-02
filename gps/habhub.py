import urllib.request as urllib2
import urllib
import json, sys, time, traceback
from base64 import b64encode
from hashlib import sha256
from datetime import datetime
import requests
import gpsd, os, time

callsign_init = False
url_habitat_uuids = "http://habitat.habhub.org/_uuids?count=%d"
url_habitat_db = "http://habitat.habhub.org/habitat/"
callsign = "CRREAT_"+os.environ.get('STATION', 'CARx')
uuids = []


gpsd.connect(host = "192.168.1.1")
pos = gpsd.get_current()
print(pos.mode)
print(pos.lat)
print(pos.lon)
print(pos.alt)
print(pos.speed)

def ISOStringNow():
    return "%sZ" % datetime.utcnow().isoformat()



def postData(doc):
    # do we have at least one uuid, if not go get more
    if len(uuids) < 1:
        fetch_uuids()

    # add uuid and uploade time
    doc['_id'] = uuids.pop()
    doc['time_uploaded'] = ISOStringNow()

    data = json.dumps(doc)
    #data = urllib.parse.urlencode(data)
    #data = data.encode('utf-8')
    headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Referer': url_habitat_db,
            }

    print("Posting doc to habitat\n%s" % json.dumps(data, indent=2))

    # req = urllib.request.Request(url_habitat_db, data, headers)
    # return urllib.request.urlopen(req, timeout=10).read()


    x = requests.post(url_habitat_db, data=data, headers = headers)
    return x.text


def fetch_uuids():

    while True:
        try:
            resp = urllib.request.urlopen(url_habitat_uuids % 10, timeout=10).read()
            data = json.loads(resp)
        except urllib.request.HTTPError as e:
            print("Unable to fetch uuids. Retrying in 5 seconds...");
            time.sleep(5)
            continue

        print("Received a set of uuids.")
        uuids.extend(data['uuids'])
        break;


def init_callsign():
    doc = {
            'type': 'listener_information',
            'time_created' : ISOStringNow(),
            'data': { 'callsign': callsign }
            }

    while True:
        try:
            resp = postData(doc)
            print("Callsign initialized.", resp)
            break;
        except urllib.request.HTTPError as e:
            print("Unable initialize callsign. Retrying in 10 seconds...");
            time.sleep(10)
            continue


def uploadPosition():
    pos = gpsd.get_current()
    if not pos.mode:
        print("Neni fix", pos)
        return

    doc = {
        'type': 'listener_telemetry',
        'time_created': ISOStringNow(),
        'data': {
            'callsign': callsign,
            'chase': True,
            'latitude': pos.lat,
            'longitude': pos.lon,
            'altitude': pos.alt,
            'speed': pos.hspeed,
        }
    }
    print(doc)
    # post position to habitat
    try:
        print(postData(doc))
    except urllib.request.HTTPError as e:
        print("Unable to upload data!")
        return

    print("Uploaded Data at: %s" % ISOStringNow())


init_callsign()

while True:
    print("Pokus o odeslani polohy")
    try:
        uploadPosition()
        time.sleep(10)
    except Exception as e:
        print("Nepovedlo se", e)
