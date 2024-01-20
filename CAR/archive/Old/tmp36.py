import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the pin you are using (replace 17 with the actual GPIO pin number)
analog_pin1 = 17
analog_pin2 = 27

# Set up the pin as an input
GPIO.setup(analog_pin1, GPIO.IN)
GPIO.setup(analog_pin2, GPIO.IN)


# Print the value
try:
    while True:
        # Read the analog value (example, you might need to use a different method depending on your sensor)
        value1 = GPIO.input(analog_pin1)
        value2 = GPIO.input(analog_pin2)

        print("")
        print(value1)
        print(value2)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopped!")
    # Clean up
    GPIO.cleanup()
