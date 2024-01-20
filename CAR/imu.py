from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
import board

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = LSM6DSOX(i2c)

def getData():

    data = (
            str(round(sensor.acceleration[0],2))
            +","+
            str(round(sensor.acceleration[1],2))
            +","+
            str(round(sensor.acceleration[2],2))
            +","+
            str(round(sensor.gyro[0],2))
            +","+
            str(round(sensor.gyro[1],2))
            +","+
            str(round(sensor.gyro[2],2))
            )

    return f"imu,{data}"