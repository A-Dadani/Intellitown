import smbus as smbus
import time

while True:
	BUS = smbus.SMBus(1)
	data = BUS.read_i2c_block_data(0x8, 0x00, 1)
	print("Color: ", data)
	time.sleep(0.4)