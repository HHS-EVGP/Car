from digitalio import DigitalInOut, Direction, Pull
import board
import busio
import adafruit_rfm9x
import time
import spidev

spi_bus = 0
spi_device = 0


spi = spidev.SpiDev()
spi.open(spi_bus,spi_device)
spi.max_speed_hz=1000000


CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spirf = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)





try:
    rfm9x = adafruit_rfm9x.RFM9x(spirf, CS, RESET, 433.0)
    rfm9x.tx_power = 23

    while True:

        send_b = 0x80
        rcv_b = spi.xfer2([send_b])

        rcv_b = spi.xfer2([send_b])
        data_r = rcv_b[0]
        if (data_r != 0x80):
            print("ERROR!"+str(data_r))





        #rfm9x.send()

        time.sleep(0.25)


except RuntimeError as error:
    print('RFM9x Error: ', error)

except KeyboardInterrupt:
    print("Stopped!")
