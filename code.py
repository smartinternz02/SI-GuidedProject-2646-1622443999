import wiotp.sdk.device
import time
import random

myConfig = { 
    "identity": {
        "orgId": "uzkg5n",
        "typeId": "ESP32",
        "deviceId":"95507"
    },
    "auth": {
        "token": "12345678"
    }
}

def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data)
    m=cmd.data
# The manual operation  ON/OFF of water pump is required in case of any SENSOR FAILURE

    if(m=={"COMMAND":"PUMPON"}):
        print("PUMP ON")
    if(m=={"COMMAND":"PUMPOFF"}):
          print("PUMP OFF")
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

while True:
    temp=random.randint(-20,125)
    hum=random.randint(0,100)
    ph_level=random.randint(0,14)
    dis=random.randint(2,400)
    mo=random.randint(0,1023)
    level=random.randint(2,400)
    waterlevel = (level/400)*100
    myData={'temperature':temp, 'humidity':hum, 'ph_level':ph_level, 'moisture':mo, 'distance':dis, 'waterlevel':waterlevel}
    time.sleep(6)
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: %s", myData)

    if mo > 600 :
        print("PUMP ON")
    else:
        print("PUMP OFF")
        
    
# Testing whether the below print statements are in sync with the IBM text to speech service OR NOT

    if dis < 50 :
     print("welcome! i am smart plant. I am happy to see you around hope you are doing well")
     time.sleep(2)
   
    if((temp < 50) and (ph_level < 5.5)):
        if((hum > 50) and (hum < 70)):
          if((mo > 400) and (mo < 600)):
             print("Smart plant is happy")
             time.sleep(3)
    else:
             print("Smart plant is sad")
             time.sleep(3)
             
    client.commandCallback = myCommandCallback
    time.sleep(1)
    
client.disconnect()
