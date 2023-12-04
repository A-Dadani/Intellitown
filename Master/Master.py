import smbus as smbus
import threading
import time
import random

runningThreads = []
slaveSI2CAddress = 0x8

def computeBusiness():
    time.sleep(2)
    return random.randint(0, 2)

def ProcessData(receivedString):
    verdict = [0, 0, 0, 0]
    verdict[0] = 1
    print("in thread : ", receivedString)
    business = computeBusiness()
    
    ##################################################
    ########### Temporary data for tesing ############
    verdict[1] = ord(receivedString[1])
    if receivedString[1] == 'n':
        verdict[2] = ord('s')
    elif receivedString[1] == 'e':
        verdict[2] = ord('w')
    elif receivedString[1] == 's':
        verdict[2] = ord('n')
    elif receivedString[1] == 'w':
        verdict[2] = ord('e')
    else:
        raise Exception("Malformated request!")
    verdict[3] = business
    ##################################################


    print("Sending ", verdict, " to slave with address, ", slaveSI2CAddress)
    bus.write_i2c_block_data(slaveSI2CAddress, 0, verdict)
    time.sleep(0.2)
    bus.close()
    current_thread = threading.current_thread()
    runningThreads.remove(current_thread)

if __name__ == '__main__':
    try:
        while True:
            try:
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
            except KeyboardInterrupt:
                raise
            except Exception as Ex:
                print(Ex)
            time.sleep(0.4)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, stopping...")
        for th in runningThreads:
            th.join()