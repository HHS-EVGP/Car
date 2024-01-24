# Last updated on 1/23/2024
import adafruit_rfm9x
import board
import busio
import os
import serial
import subprocess
import time
from digitalio import DigitalInOut, Direction, Pull
import sys
import logging

import imu
import arduino

time_imu = time.time()
time_bp = time.time()
time_temps = time.time()
time_ca = time.time()

try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
except:
    try:
        ser = serial.Serial('/dev/ttyACM1', 9600, timeout=0)
    except Exception as noArduino:
        print("There seems to be no Arduino ):")
        exit()

ser.reset_input_buffer()

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Configure RFM9x LoRa Radio

CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 433.0, high_power = True)
rfm9x.tx_power = 23

running = True

dataR = None

index = 1
conter = 0
while os.path.exists(f"/home/car/2024{index}.data.log"):
    index += 1
new_file_name = f"/home/car/2024/{index}.data.log"

logging.basicConfig(filename=new_file_name, filemode='w', format='%(message)s')


def sendRF(data):

    print(data)

    rfm9x.send(bytearray(data,'utf-8'))

    logging.warning(data)


while running:

    time.sleep(0.25)

    data_2_send = arduino.getData(ser)
    data_2_send += "|"
    data_2_send += imu.getData()
    

    sendRF(data_2_send)


    
    
    
