#!/usr/bin/python
# This is only executed on the device client e.g. Raspberry Pi
import time
import os, json
import ibmiotf.application
import ibmiotf.device
import uuid
import motionSensor

client = None


motionSensorGPIOPort = 14

#####################################
#FILL IN THESE DETAILS
#####################################

organization = "xxxxx"
deviceType = "rasp"
deviceId = "rasp01"
appId = str(uuid.uuid4())
authMethod = "token"
authToken = "xxxx"

try:
  deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
  client = ibmiotf.device.Client(deviceOptions)
  print "try to connect to IoT"
  client.connect()
  print "connect to IoT successfully"

  motionStatus = False
  motionSensor.setup(motionSensorGPIOPort)


  while True:
    motionData = motionSensor.sample()
    jsonMotionData = json.dumps(motionData)
    client.publishEvent("status", "json", jsonMotionData)
#    client.publishEvent("rasp", deviceId, "motionSensor", "json", jsonMotionData)

    if motionData['motionDetected'] != motionStatus:
      motionStatus = motionData['motionDetected']
      print "Change in motion detector status, motionDetected is now:", motionStatus

    time.sleep(0.2)

except ibmiotf.ConnectionException as e:
 print e

