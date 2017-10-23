import RPi.GPIO as gpio
import time
gpio.cleanup()
gpio.setmode(gpio.BOARD)

gpio.setup(7,gpio.OUT)

#fires off
while 1:
    gpio.output(7,0)
    time.sleep(0.2)
    gpio.output(7,1)
    time.sleep(0.2)
