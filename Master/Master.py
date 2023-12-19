import paho.mqtt.client as mqtt
import smbus as smbus
import threading
import time
import base64
import random
from PIL import Image
import requests
import json
import datetime
import traceback

runningThreads = []
slaveSI2CAddress = 0x8

i2c_lock = threading.Lock()

mqtt_broker_ip = "192.168.193.114"
mqtt_port = 1883
mqtt_client_id = "Raspberrypi0"

mqtt_NS_request = "NSREQ"
mqtt_EW_request = "EWREQ"
mqtt_WE_request = "WEREQ"
mqtt_SN_request = "SNREQ"
mqtt_SE_request = "SEREQ"
mqtt_SW_request = "SWREQ"

mqtt_NS_response = "NSRES"
mqtt_EW_response = "EWRES"
mqtt_WE_response = "WERES"
mqtt_SN_response = "SNRES"
mqtt_SE_response = "SERES"
mqtt_SW_response = "SWRES"

mqtt_NS_image_path = "intersectionNS.jpg"
mqtt_EW_image_path = "intersectionEW.jpg"
mqtt_WE_image_path = "intersectionWE.jpg"
mqtt_SN_image_path = "intersectionSN.jpg"
mqtt_SE_image_path = "intersectionSE.jpg"
mqtt_SW_image_path = "intersectionSW.jpg"

mqtt_isNSreceived = True
mqtt_isEWreceived = True
mqtt_isWEreceived = True
mqtt_isSNreceived = True
mqtt_isSEreceived = True
mqtt_isSWreceived = True

NSLock = threading.Lock()
EWLock = threading.Lock()
WELock = threading.Lock()
SNLock = threading.Lock()
SELock = threading.Lock()
SWLock = threading.Lock()

url = 'https://myapp-ckfcrjehrq-ew.a.run.app/detect'

bus = smbus.SMBus(1)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(mqtt_NS_response)
            print(f"Subscribed to {mqtt_NS_response}")
            client.subscribe(mqtt_EW_response)
            print(f"Subscribed to {mqtt_EW_response}")
            client.subscribe(mqtt_WE_response)
            print(f"Subscribed to {mqtt_WE_response}")
            client.subscribe(mqtt_SN_response)
            print(f"Subscribed to {mqtt_SN_response}")
            client.subscribe(mqtt_SE_response)
            print(f"Subscribed to {mqtt_SE_response}")
            client.subscribe(mqtt_SW_response)
            print(f"Subscribed to {mqtt_SW_response}")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt.Client(mqtt_client_id)
    client.on_connect = on_connect
    client.connect(mqtt_broker_ip, mqtt_port, 60)
    return client

def on_message(client, userdata, msg):
    global mqtt_isNSreceived, mqtt_isEWreceived, mqtt_isWEreceived, mqtt_isSNreceived, mqtt_isSEreceived, mqtt_isSWreceived
    if msg.topic == mqtt_NS_response:
        save_base64_image(msg.payload.decode('utf-8'), mqtt_NS_image_path)
        print(f"Image received NS")
        with NSLock:
            mqtt_isNSreceived = True
        print("set flag")
    elif msg.topic == mqtt_EW_response:
        save_base64_image(msg.payload.decode('utf-8'), mqtt_EW_image_path)
        print(f"Image received EW")
        with EWLock:
            mqtt_isEWreceived = True
    elif msg.topic == mqtt_WE_response:
        save_base64_image(msg.payload.decode('utf-8'), mqtt_WE_image_path)
        print(f"Image received WE")
        with WELock:
            mqtt_isWEreceived = True
    elif msg.topic == mqtt_SN_response:
        save_base64_image(msg.payload.decode('utf-8'), mqtt_SN_image_path)
        print(f"Image received SN")
        with SNLock:
            mqtt_isSNreceived = True
    elif msg.topic == mqtt_SE_response:
        save_base64_image(msg.payload.decode('utf-8'), mqtt_SE_image_path)
        print(f"Image received SE")
        with SELock:
            mqtt_isSEreceived = True
    elif msg.topic == mqtt_SW_response:
        save_base64_image(msg.payload.decode('utf-8'), f"intersectionSW.jpg")
        print(f"Image received SW")
        with SWLock:
            mqtt_isSWreceived = True

client = connect_mqtt()
client.on_message = on_message
client.loop_start()

def save_base64_image(base64_string, filename):
    image_data = base64.b64decode(base64_string)
    with open(filename, "wb") as image_file:
        image_file.write(image_data)

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def computeBusiness(base64_img_string):
    payload = json.dumps({
        "image": base64_img_string
    })

    headers = {
        'Content-Type': 'application/json'
    }
    print("Sending request...")
    response = requests.post(url, headers=headers, data=payload)
    print(response.json()['vehicle_count'])
    return response.json()['vehicle_count'];

def ProcessData(receivedString):
    global mqtt_isNSreceived, mqtt_isEWreceived, mqtt_isWEreceived, mqtt_isSNreceived, mqtt_isSEreceived, mqtt_isSWreceived
    verdict = [0, 0, 0, 0]
    verdict[0] = 1
    print("in thread : ", receivedString)
    verdict[1] = ord(receivedString[0])
    verdict[2] = ord(receivedString[1])

    img = None

    
    if receivedString[0] == 'e':
        if receivedString[1] == 'w':
            client.publish(mqtt_EW_request, payload="capture_photo")
            EW_start_time = datetime.datetime.now()
            with EWLock:
                mqtt_isEWreceived = False
            while not mqtt_isEWreceived:
                elapsed_time = datetime.datetime.now() - EW_start_time
                if elapsed_time.total_seconds() > 10:
                    print("EW timed out")
                    mqtt_isEWreceived = True
                    current_thread = threading.current_thread()
                    runningThreads.remove(current_thread)
                    return
            print("EW PASSED")
            img = get_base64_image(mqtt_EW_image_path)
        else: 
            print("Warning! unsupported request")
            return
    elif receivedString[0] == 'n':
        if receivedString[1] == 's':
            print("in north south")
            client.publish(mqtt_NS_request, payload="capture_photo")
            NS_start_time = datetime.datetime.now()
            with NSLock:
                mqtt_isNSreceived = False
            while not mqtt_isNSreceived:
                elapsed_time = datetime.datetime.now() - NS_start_time
                if elapsed_time.total_seconds() > 10:
                    print("NS timed out")
                    mqtt_isNSreceived = True
                    current_thread = threading.current_thread()
                    runningThreads.remove(current_thread)
                    return
            print("passed NS")
            img = get_base64_image(mqtt_NS_image_path)
        else: 
            print("Warning! unsupported request")
            return
    elif receivedString[0] == 'w':
        if receivedString[1] == 'e':
            client.publish(mqtt_WE_request, payload="capture_photo")
            WE_start_time = datetime.datetime.now()
            with WELock:
                mqtt_isWEreceived = False
            while not mqtt_isWEreceived:
                elapsed_time = datetime.datetime.now() - WE_start_time
                if elapsed_time.total_seconds() > 10:
                    print("WE timed out")
                    mqtt_isWEreceived = True
                    current_thread = threading.current_thread()
                    runningThreads.remove(current_thread)
                    return
            img = get_base64_image(mqtt_WE_image_path)
        else:
            print("Warning! unsupported request")
            return
    else:
        print("Warning! unsupported request")
        return

    # image should be received and saved to variable img

    print("about to compute business")
    business = computeBusiness(img)

    if business == 0:
        verdict[3] = 0
    elif business == 1:
        verdict[3] = 1
    else:
        verdict[3] = 2    

    print("Sending ", verdict, " to slave with address, ", slaveSI2CAddress)
    with i2c_lock:
        bus.write_i2c_block_data(slaveSI2CAddress, 0, verdict)
    time.sleep(0.2)
    current_thread = threading.current_thread()
    runningThreads.remove(current_thread)

def main():
    with i2c_lock:
        received_data = bus.read_i2c_block_data(slaveSI2CAddress, 0, 3)
    print("outside : ", received_data)
    
    if (received_data[0] == 1):
        if chr(received_data[2]) == 'n':
            if mqtt_isNSreceived:
                i2cThread1 = threading.Thread(target=ProcessData, args=('ns',))
                i2cThread1.start()
                runningThreads.append(i2cThread1)
        elif chr(received_data[2]) == 'e':
            if mqtt_isEWreceived:
                i2cThread1 = threading.Thread(target=ProcessData, args=('ew',))
                i2cThread1.start()
                runningThreads.append(i2cThread1)
            if mqtt_isWEreceived:
                i2cThread2 = threading.Thread(target=ProcessData, args=('we',))
                i2cThread2.start()
                runningThreads.append(i2cThread2)

if __name__ == '__main__':
    try:
        while True:
            try:
                main()
            except KeyboardInterrupt:
                raise
            except Exception as Ex:
                #print(Ex)
                traceback.print_exc()
            time.sleep(0.4)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, stopping...")
        for th in runningThreads:
            print("Joined and waiting for thread", th)
            th.join()
    except Exception as Ex:
        print(Ex)