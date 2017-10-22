import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD) #BOARD is the physical numbering ofpins on the board
#while gpio.BCM is the I/O name of the pin, i recommend BOARD

#to set up the channel as output:
gpio.setup(18, gpio.OUT)

#you can also set up multiple channels as out with a list

#I/O
#to input:
#gpio.input(channel)

#output: (here channel is 1)
gpio.output(18,True)

#it is always important to clean up afterwards:
#done=input('Press enter when finished: ')
#gpio.cleanup()
#use gpio.cleaup(channel) to clean up specific channels

