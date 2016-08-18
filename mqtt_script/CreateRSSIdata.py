#!/usr/bin/python

import criotdm
import ciotdm
import json
import threading
from random import randint

# Set varibles
httpuser = "admin"
httppass = "admin"
rt_container       = 3
rt_contentInstance = 4
rssipayload = '''
{
  "GpsThread": {
    "altitude": %s,
    "gps_qual": %s,
    "altitude_units": "M",
    "geo_sep_units": "M",
    "true_course": "%s",
    "lon": "%s",
    "type": "gpsData",
    "num_sats": "09",
    "version": "0.0.9",
    "mag_var_dir": "",
    "ref_station_id": "0000",
    "datestamp": "140716",
    "age_gps_data": "",
    "geo_sep": "49.0",
    "lat_dir": "N",
    "horizontal_dil": "1.1",
    "lon_dir": "E",
    "mag_variation": "",
    "spd_over_grnd": "0.00",
    "lat": "%s",
    "status": "A",
    "timestamp": 1468497589.99156
  },
  "PpsThread": {
    "type": "ppsHigh",
    "version": "0.0.9",
    "timestamp": 1468497590.400244
  },
  "LoraRxThread": {
    "SF12": {
      "RSSI": %s,
      "timestamp": "2016-06-29 23:46:27.127Z"
    },
    "SF8": {
      "RSSI": %s,
      "timestamp": "2016-07-12 12:56:25.230Z"
    },
    "SF10": {
      "RSSI": %s,
      "timestamp": "2016-07-12 12:56:35.683Z"
    },
    "SF7": {
      "RSSI": %s,
      "timestamp": "2016-06-29 23:46:30.615Z"
    },
    "SF11": {
      "RSSI": %s,
      "timestamp": "2016-07-12 12:56:41.428Z"
    },
    "SF9": {
      "RSSI": %s,
      "timestamp": "2016-07-12 12:56:30.362Z"
    }
  },
  "deviceName": "wuData",
  "version": "0.0.9"
}
'''

fakelatStart = 4657
fakelngSatrt = 55
global fakelat
global fakelng
fakelat = fakelatStart
fakelng = fakelngSatrt
def create_container(parent, container_name):
	attr = '"rn":%s, "mni":3' %(container_name)
	container_resp = connect.create(parent, rt_container, attr)
	# print container_resp.text

def create_cin():
    threading.Timer(5.0,create_cin).start()
    fakeAltitude = randint(200, 250)
    fakeGPSquality = randint(1,3)
    fakeTruecourse = randint(200,300)
    global fakelat
    global fakelng
    if fakelng > 550:
        fakelat = fakelatStart
        fakelng = fakelngSatrt
    fakelng = fakelng + 0.2 + randint(0,5) * 0.01
    fakelat = fakelat + randint(-5, 5) * 0.02
    payload = rssipayload % (fakeAltitude, fakeGPSquality, fakeTruecourse, fakelng, fakelat, randint(0,9), randint(0,19), randint(10,19), randint(20,29), randint(0,29), randint(0,19))
    attr = '"con":%s' %(payload)
    print payload
    payloadjson = json.loads(payload)
    path = inputPath + "/" + payloadjson['deviceName']
    connect.create(path, rt_contentInstance, attr)
    print criotdm.text(connect.response)
    if criotdm.status_code(connect.response) > 299:
        create_container(inputPath, payloadjson['deviceName'])
        connect.create(path, rt_contentInstance, attr)


def getCSEName(path):
	return path.split('/')[0]

def createContainerPath(path):
	pathArray = path.split('/')
	print pathArray
	parent = CSEName
	for resource in pathArray:
		create_container(parent, resource)
		parent = parent + "/" + resource

inputHost = raw_input("Please enter the IP address of your IOTDM: (like localhost,168.128.108.104)")
inputPath = raw_input("Please enter the path of IOTDM to store the data(like InCSE1/MQTTMessage):")

CSEName = getCSEName(inputPath)
connect = ciotdm.connect(inputHost, base=CSEName, auth=(httpuser, httppass), protocol="http")
createContainerPath(inputPath.lstrip(CSEName+"/"))
create_cin()