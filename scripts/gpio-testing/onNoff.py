import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD) #BOARD is for the physical on board pin number
pin=int(raw_input('Which pin would you like to toggle? '))
gpio.setup(pin,gpio.OUT)
#apparently u cannot control pin 1
op=''
while op!='e':
    op=raw_input('0 for off, 1 for on and e for exit: ')
    if op=='0':
        gpio.output(pin,0)
        
    elif op=='1':
        gpio.output(pin,1)
        
    
gpio.cleanup()

