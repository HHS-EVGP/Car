import adafruit_rfm9x
import board
import busio
import os
import serial
import subprocess
import time
from digitalio import DigitalInOut, Direction, Pull

import imu
import arduino

time_imu = time.time()
time_bp = time.time()
time_temps = time.time()
time_ca = time.time()

try:
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0)
except:
    ser = serial.Serial('/dev/ttyACM1', 115200, timeout=0)

ser.reset_input_buffer()

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# # Configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 433.0, high_power = True)
rfm9x.tx_power = 20

running = True

dataR = None

def sendRF(data):
    if data: 
        if data == None:
            return
        if type(data) is tuple:
            for send in data:
                # print(send)
                # print("Good Send")
                rfm9x.send(bytearray(send,'utf-8'))
        else:
            # print(data)
            # print("Good Send")
            rfm9x.send(bytearray(data,'utf-8'))

while running:

    # if time.time() - time_imu > 0.5:
    #     time_imu = time.time()
    #     data = imu.getData()
    #     sendRF(data)
    #     print("Sent: IMU")
    
    # if time.time() - time_ca > 0.5:
    #     time_ca = time.time()
    #     data = arduino.getData_ca(ser)
    #     sendRF(data)
    #     print("Sent: CA")
    
    # if time.time() - time_bp > 0.5:
    #     time_bp = time.time()
    #     data = arduino.getData_bp(ser)
    #     sendRF(data)
    #     print("Sent: BP")
    
    speeds = 0.25

    if time.time() - time_imu > 0.5:
        time_imu = time.time()
        data = imu.getData()
        sendRF(data)
        print("Sent: IMU")
        time.sleep(speeds)
        time_ca = time.time()
        data = arduino.getData_ca(ser)
        sendRF(data)
        time.sleep(speeds)
        print("Sent: CA")
        time_bp = time.time()
        data = arduino.getData_bp(ser)
        sendRF(data)
        print("Sent: BP")
        time.sleep(speeds)


    if time.time() - time_temps > 5:
        time_temps = time.time()
        data = arduino.getData_temps(ser)
        sendRF(data)
        print("Sent: TEMPS")


    
    
    
