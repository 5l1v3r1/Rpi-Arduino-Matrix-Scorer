'''countdown'''

import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD)

#pins used
pins=[7,11,13,15,29,31,33]
p1=[7,11,15,31]
p2=[7,13,15,29,31]
p3=[7,13,15,31,33]
p4=[11,13,15,33]
p5=[7,11,15,31,33]
p6=[7,11,15,29,31,33]
p7=[7,11,13,33]
p8=pins
p9=[7,11,13,15,33]
p0=[7,11,13,29,31,33]

for i in pins:
    gpio.setup(i, gpio.OUT)
gpio.output(pins,0)

#example: gpio.output(7,1)

#functions to display numbers


def lit(i):
    gpio.output(pins,0)
    exec('gpio.output(p%s,1)'%i)
    
def nth():
    for i in pins:
        gpio.output(i,0)
        
#nums=['0','1','2','3','4','5','6','7','8','9']

#countdown starts here
lit('3')
time.sleep(1)
lit('2')
time.sleep(1)
lit('1')
time.sleep(1)
lit('0')
time.sleep(1)

#BOOM
for i in range(10):
    nth()
    time.sleep(0.2)
    lit('8')
    time.sleep(0.2)
        
gpio.cleanup()        
      



        
