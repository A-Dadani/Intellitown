import paho.mqtt.client as mqtt
import smbus as smbus
import threading
import time
import base64
import random
from PIL import Image

runningThreads = []
slaveSI2CAddress = 0x8

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

mqtt_isNSreceived = False
mqtt_isEWreceived = False
mqtt_isWEreceived = False
mqtt_isSNreceived = False
mqtt_isSEreceived = False
mqtt_isSWreceived = False

NSLock = threading.Lock()
EWLock = threading.Lock()
WELock = threading.Lock()
SNLock = threading.Lock()
SELock = threading.Lock()
SWLock = threading.Lock()

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
    if msg.topic == mqtt_NS_response:
        save_base64_image(msg.payload.decode('utf-8'), mqtt_NS_image_path)
        print(f"Image received NS")
        with NSLock:
            mqtt_isNSreceived = True
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

def get_base64_image(filepath):
    with open(filepath, "rb") as f:
        image = Image.open(f)
        rotated_image = image.rotate(90)
        rotated_image_data = rotated_image.tobytes()
        base64_encoded = base64.b64encode(rotated_image_data)
        return base64_encoded.decode('utf-8')

######### TEMPORARY FOR TESTING ###############
def computeBusiness(base64_img_string):
    time.sleep(2)
    return random.randint(0, 2)
####################################################

def ProcessData(receivedString):
    verdict = [0, 0, 0, 0]
    verdict[0] = 1
    print("in thread : ", receivedString)

    verdict[1] = ord(receivedString[1])

    img = None

    if receivedString[0] == 's':
        if receivedString[1] == 'n':
            client.publish(mqtt_SN_request, payload="capture_photo")
            with SNLock:
                mqtt_isSNreceived = False
            while not mqtt_isSNreceived:
                pass
            img = get_base64_image(mqtt_SN_image_path)
        elif receivedString[1] == 'e':
            client.publish(mqtt_SE_request, payload="capture_photo")
            with SELock:
                mqtt_isSEreceived = False
            while not mqtt_isSEreceived:
                pass
            img = get_base64_image(mqtt_SE_image_path)
        elif receivedString[1] == 'w':
            client.publish(mqtt_SW_request, payload="capture_photo")
            with SWLock:
                mqtt_isSWreceived = False
            while not mqtt_isSWreceived:
                pass
            img = get_base64_image(mqtt_SW_image_path)
        else: 
            print("Warning! unsupported request")
            return
    elif receivedString[0] == 'e':
        if receivedString[1] == 'w':
            client.publish(mqtt_EW_request, payload="capture_photo")
            with EWLock:
                mqtt_isEWreceived = False
            while not mqtt_isEWreceived:
                pass
            img = get_base64_image(mqtt_EW_image_path)
        else: 
            print("Warning! unsupported request")
            return
    elif receivedString[0] == 'n':
        if receivedString[1] == 's':
            client.publish(mqtt_NS_request, payload="capture_photo")
            with NSLock:
                mqtt_isNSreceived = False
            while not mqtt_isNSreceived:
                pass
            img = get_base64_image(mqtt_NS_image_path)
        else: 
            print("Warning! unsupported request")
            return
    elif receivedString[0] == 'w':
        if receivedString[1] == 'e':
            client.publish(mqtt_WE_request, payload="capture_photo")
            with WELock:
                mqtt_isWEreceived = False
            while not mqtt_isWEreceived:
                pass
            img = get_base64_image(mqtt_WE_image_path)
        else:
            print("Warning! unsupported request")
            return
    else:
        print("Warning! unsupported request")

    # image should be received and saved to variable img

    ######### TEMPORARY FOR TESTING ###############
    business = computeBusiness(img)
    ####################################################

    verdict[3] = business
    

    print("Sending ", verdict, " to slave with address, ", slaveSI2CAddress)
    #bus.write_i2c_block_data(slaveSI2CAddress, 0, verdict)
    time.sleep(0.2)
    bus.close()
    current_thread = threading.current_thread()
    runningThreads.remove(current_thread)

def main():
    bus = smbus.SMBus(1)
    received_data = bus.read_i2c_block_data(slaveSI2CAddress, 0, 3)
    print("outside : ", received_data)
    
    if (received_data[0] == 1):
        if chr(received_data[2]) == 'n':
            i2cThread1 = threading.Thread(target=ProcessData, args=(chr(received_data[1]) + 'n',))
            i2cThread1.start()
            runningThreads.append(i2cThread1)
            i2cThread2 = threading.Thread(target=ProcessData, args=(chr(received_data[1]) + 's',))
            i2cThread2.start()
            runningThreads.append(i2cThread2)
        elif chr(received_data[2]) == 'e':
            i2cThread1 = threading.Thread(target=ProcessData, args=(chr(received_data[1]) + 'e',))
            i2cThread1.start()
            runningThreads.append(i2cThread1)
            i2cThread2 = threading.Thread(target=ProcessData, args=(chr(received_data[1]) + 'w',))
            i2cThread2.start()
            runningThreads.append(i2cThread2)
                 
               
#    i2cThread1 = threading.Thread(target=ProcessData, args=("sn",))
#    i2cThread1.start()
#    runningThreads.append(i2cThread1)
#    print("Main thread sleeping...")
#    time.sleep(5)
#    print("Main thread wakes up")

if __name__ == '__main__':
    try:
        while True:
            try:
                main()
            except KeyboardInterrupt:
                raise
            except Exception as Ex:
                print(Ex)
            time.sleep(0.4)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, stopping...")
        for th in runningThreads:
            print("Joined and waiting for thread", th)
            th.join()
    except Exception as Ex:
        print(Ex)