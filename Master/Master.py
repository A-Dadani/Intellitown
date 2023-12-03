import smbus as smbus
import time

while True:
	bus = smbus.SMBus(1)
	received_data = bus.read_i2c_block_data(0x8, 0, 5)
	print(received_data)
	time.sleep(0.4)