from digitalio import DigitalInOut, Direction, Pull
import board
import busio
import adafruit_rfm9x
import time
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = LSM6DSOX(i2c)


try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 433.0)
    rfm9x.tx_power = 23

    while True:

        rfm9x.send(bytearray(
            f"$imu" + 
            str(sensor.acceleration[0])
            +","+
            str(sensor.acceleration[1])
            +","+
            str(sensor.acceleration[2])
            +","+
            str(sensor.gyro[0])
            +","+
            str(sensor.gyro[1])
            +","+
            str(sensor.gyro[2]),
            'utf-8'
            ))

        time.sleep(0.25)
        

except RuntimeError as error:
    print('RFM9x Error: ', error)

except KeyboardInterrupt:
    print("Stopped!")
