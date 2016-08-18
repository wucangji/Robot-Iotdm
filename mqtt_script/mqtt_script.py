#!/usr/bin/python

import criotdm
import ciotdm
import paho.mqtt.subscribe as subscribe
import json

# Set varibles
httphost = "localhost"
httpuser = "admin"
httppass = "admin"
rt_container       = 3
rt_contentInstance = 4



def create_container(parent, container_name):
	attr = '"rn":%s' %(container_name)
	container_resp = connect.create(parent, rt_container, attr)
	# print container_resp.text

def create_cin(parentpath, payload):
	attr = '"con":%s' %(payload)
	payloadjson = json.loads(payload)
	print(payloadjson['deviceName'])
	path = parentpath + "/" + payloadjson['deviceName']
	connect.create(path, rt_contentInstance, attr)
	print criotdm.text(connect.response)
	if criotdm.status_code(connect.response) > 299:
		create_container(parentpath, payloadjson['deviceName'])
		connect.create(path, rt_contentInstance, attr)

def on_message_print(client, userdata, message):
	print("%s %s" % (message.topic, message.payload))
	create_cin(inputPath, message.payload)

def getCSEName(path):
	return path.split('/')[0]

def createContainerPath(path):
	pathArray = path.split('/')
	print pathArray
	parent = CSEName
	for resource in pathArray:
		create_container(parent, resource)
		parent = parent + "/" + resource

inputHost = raw_input("Please enter the hostname of the MQTT broker (like 168.128.108.105):")
inputPort = raw_input("Please enter the port number (like 1883):")
inputTopic = raw_input("Please enter the topic you want to subscribe (like /tdf/test):")
inputPath = raw_input("Please enter the path of IOTDM to store the data(like InCSE1/MQTTMessage):")

CSEName = getCSEName(inputPath)
connect = ciotdm.connect(httphost, base=CSEName, auth=(httpuser, httppass), protocol="http")
createContainerPath(inputPath.lstrip(CSEName+"/"))
subscribe.callback(on_message_print, topics = inputTopic, hostname = inputHost, port = inputPort)
# subscribe.callback(on_message_print, topics = "/tdf/test", hostname = "168.128.108.105", port = 1883)