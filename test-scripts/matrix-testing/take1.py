'''
This is the first take to drive the 16x32 LED matrix with my raspberry pi.
The goal is to just get something lit up on the screen :)
Using red light so only R1 set to be on output.

example JS code on tuicool.com:
while(1){
    for(var i = 0; i < 16; i++){
        LATCH = 0; 
        for(var j = 0; j < 16; j++){
            R1 = <position output>
            
            SCK = 0;
            SCK = 1;         
        }

        OE = 1; 
        ROW = i;   
        LATCH = 1; 
        OE = 0; 
    }
}

'''

import RPi.GPIO as GPIO
import time,datetime


#set the gpio mode to BOARD (physical pin numbering, you are counting it)
GPIO.setmode(GPIO.BOARD)

#setup all the pins used into output mode
pins=[3,5,29,31,33,35,11,36] #OE,CLK,A,B,C,D,R1,STB(Latch)
GPIO.setup(pins, GPIO.OUT)

#set variable names for specific pins
OE=3
CLK=5
rows=[29,31,33,35]

A=29
B=31
C=33
D=35

R1=11
STB=36



#functions for converting an integer value into 16bit ABCD pin

def rowconv(val):
	val=bin(val)
	val=list(val.lstrip('0b'))
	print(val)
	if len(val)<4:
		for i in range (4-len(val)):
			val.insert(i,0)
	print(val)
	return val
	
	
	


rowconv(02)

#setup the positions of the lights, as the list 'image'
image=[]
row=[]

for c in range(32):
	row.append(0);
for r in range(16):
	image.append(row)

'''	
image[2][0]=1	#the first LED on the third row should be lit
image[2][1]=1
image[2][2]=1
'''

for a in range(16):
	image[10][a]=0

#displays the image

'''
for times in range(500):
	for j in range(16):
		GPIO.output(STB,0) 
		for i in range(32):
			GPIO.output(R1,image[j][i]) #[31-i]
			GPIO.output(CLK,0)
			GPIO.output(CLK,1)	
			print('i:',i) #debug
			
		GPIO.output(OE,1)
		
		
		GPIO.output(rows,j)
		GPIO.output(STB,1)
		GPIO.output(OE,0)
		
		print('j:',j)

'''

for times in range(400):
	for j in range(16):
		GPIO.output(STB,0) 
		for i in range(32):
			GPIO.output(R1,image[j][i]) #[31-i]
			GPIO.output(CLK,0)
			GPIO.output(CLK,1)	
			#print('i:',i) #debug
			
		GPIO.output(OE,1)
		
		GPIO.output(D, int(rowconv(j)[0]))
		GPIO.output(C, int(rowconv(j)[1]))
		GPIO.output(B, int(rowconv(j)[2]))
		GPIO.output(A, int(rowconv(j)[3]))
		
		#GPIO.output(rows,j)
		
		GPIO.output(STB,1)
		GPIO.output(OE,0)
		
		#print('j:',j)

GPIO.cleanup()
print('Done')

	






