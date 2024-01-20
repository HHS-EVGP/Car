from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
import board

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = LSM6DSOX(i2c)

def getData():

    data = (
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
            str(sensor.gyro[2])
            )

    return f"imu,{data}"