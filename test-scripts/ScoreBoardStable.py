#!/usr/bin/python
'''
A script for displaying score on the LED matrix

0.1.5:
-Puts the code into 2 classes for tidying: one for display and setup, one for database connection

'''

import RPi.GPIO as GPIO
import time,sys,MySQLdb
import numpy as np



#################################### MATRIX CLASS ###################################################


class Matrix:

    def __init__(self):

        global image,TAList,TBList,TCList,TDList,AList,BList,CList,DList,TColon,Colon


        #TA1-7 are the lists of coordinates for the timer.
        TA1=[[0,6],[0,7],[0,8],[0,9]]
        TA2=[[0,6],[1,6],[2,6]]
        TA3=[[2,6],[2,7],[2,8],[2,9]]
        TA4=[[3,6],[4,6]]
        TA5=[[4,6],[4,7],[4,8],[4,9]]
        TA6=[[3,9],[4,9]]
        TA7=[[0,9],[1,9],[2,9]]
        #TAList (Time-A-List) includes all the sublists of the coordinates.
        TAList=[TA1,TA2,TA3,TA4,TA5,TA6,TA7]

        #TB1-7 are the second list of coordinates
        #Defining all 7 sublists in one line
        TB1,TB2,TB3,TB4,TB5,TB6,TB7 = [],[],[],[],[],[],[] 
        #Putting them all together in BList
        TBList=[TB1,TB2,TB3,TB4,TB5,TB6,TB7]

        #putting values in TBList according to TAList (from their mathmetical relationship)
        #7 is the length of the lists, r is row and c is column of the coordinates.
        for i in range(7):
            for r,c in TAList[i]:
                TBList[i].append([r,c+5])

        #Now do the same with TCList according to its relationship with TBList:
        TC1,TC2,TC3,TC4,TC5,TC6,TC7 = [],[],[],[],[],[],[]
        TCList=[TC1,TC2,TC3,TC4,TC5,TC6,TC7]
        for i in range(7):
            for r,c in TBList[i]:
                #This one is c+7 because there's the colon in between
                TCList[i].append([r,c+7]) 

        #And TDList:
        TD1,TD2,TD3,TD4,TD5,TD6,TD7 = [],[],[],[],[],[],[]
        TDList=[TD1,TD2,TD3,TD4,TD5,TD6,TD7]
        for i in range(7):
            for r,c in TCList[i]:
                TDList[i].append([r,c+5]) 
        #TColon is the colon between the minutes and seconds
        TColon=[[1,16],[3,16]]


        #Now for the scoring(same logic as above):
        #<Scoring section>
        A1=[[6,3],[6,4],[6,5],[6,6],[6,7]]
        A2=[[6,3],[7,3],[8,3],[9,3],[10,3]]
        A3=[[10,3],[10,4],[10,5],[10,6],[10,7]]
        A4=[[10,3],[11,3],[12,3],[13,3],[14,3]]
        A5=[[14,3],[14,4],[14,5],[14,6],[14,7]]
        A6=[[10,7],[11,7],[12,7],[13,7],[14,7]]
        A7=[[6,7],[7,7],[8,7],[9,7],[10,7]]
        AList=[A1,A2,A3,A4,A5,A6,A7]

        B1,B2,B3,B4,B5,B6,B7 = [],[],[],[],[],[],[]
        BList=[B1,B2,B3,B4,B5,B6,B7]

        for i in range(7):
            for r,c in AList[i]:
                BList[i].append([r,c+6])

        C1,C2,C3,C4,C5,C6,C7 = [],[],[],[],[],[],[]
        CList=[C1,C2,C3,C4,C5,C6,C7]

        for i in range(7):
            for r,c in BList[i]:
                CList[i].append([r,c+10])

        D1,D2,D3,D4,D5,D6,D7 = [],[],[],[],[],[],[]
        DList=[D1,D2,D3,D4,D5,D6,D7]
        for i in range(7):
            for r,c in CList[i]:
                DList[i].append([r,c+6])

        Colon=[[8,16],[12,16]]
        #</Scoring section>


        #setup the positions of the lights, as the 2d array 'image'
        image=np.ones((16,32))
        image=image.tolist()

        #<debug>
        '''
        print "\nTAList:",TAList
        print "\nTBList:",TBList
        print "\nTCList:",TCList
        print "\nTDList:",TDList

        print "\nAList:",AList
        print "\nBList:",BList
        print "\nCList:",CList
        print "\nDList:",DList
        '''
        #</debug>

        #Sets up a public dictionary (self.) for the numbers 
        #<number to display> : <elements to turn to ON state>
        self.numdic={
        '0':'1,2,4,5,6,7',
        '1':'6,7', 
        '2':'1,3,4,5,7',
        '3':'1,3,5,6,7',
        '4':'2,3,6,7',
        '5':'1,2,3,5,6',
        '6':'1,2,3,4,5,6',
        '7':'1,6,7',
        '8':'1,2,3,4,5,6,7',
        '9':'1,2,3,5,6,7'}

    def reset(self):
        '''
        This function resets the image to its original state (also used to initialist it) 
        '''
        global image,TAList,TBList,TCList,TDList,AList,BList,CList,DList,TColon,Colon

        #turns the coordinates of the points needing to be displayed into 1 (to turn those bulbs OFF)
        #With a nested loop at one go..

        for i in [TAList,TBList,TCList,TDList,AList,BList,CList,DList]:
            for a in i:
                for row,column in a:
                    image[row][column]=1

        #colons are always on so we output a 0.
        for row,column in TColon:
            image[row][column]=0
        for row,column in Colon:
            image[row][column]=0

        #<debug>    
        #print "Image",image
        #</debug>


                                      
        #print(a,b,c,d)'''

    def rowconv(self,val):
        '''functions that takes a decimal value and convert it into a list of 4 binaries.
        '''

        #convert from int to binary
        val=bin(val)
        #removes the 0b   
        val=list(val.lstrip('0b'))   

        if len(val)<4:
            for i in range (4-len(val)):
                val.insert(i,0)

        #returns the list
        return val   


    

    def ChangeScore(self,score1,score2):
        '''
        function to change the score on the display according to the arguments $score1 and $score2
        '''
        global image,AList,BList,CList,DList

        #converts the score into 4 digits a,b,c and d (2 Digits each team)
        
        if len(str(score1))<2:
            a=0
            b=score1
        else:
            a=int(str(score1)[0])
            b=int(str(score1)[1])

        if len(str(score2))<2:
            c=0
            d=score2
        else:
            c=int(str(score2)[0])
            d=int(str(score2)[1])

        #The logic below is the same as the function ChangeTime
        #for all the values of self.numdic with key a (the number to display)
        for i in self.numdic[str(a)].split(','):
            for row,column in AList[int(i)-1]:
                image[row][column]=0

        for i in self.numdic[str(b)].split(','):
            for row,column in BList[int(i)-1]:
                image[row][column]=0

        for i in self.numdic[str(c)].split(','):
            for row,column in CList[int(i)-1]:
                image[row][column]=0

        for i in self.numdic[str(d)].split(','):
            for row,column in DList[int(i)-1]:
                image[row][column]=0

    def ChangeTime(self,m,s):
        ''' 
        function that converts the minute and seconds string, each 2 digits, into the image for output.
        The input, m and s, must be a 2 digit integer.
        '''
        global image,TAList,TBlist,TClist,TDlist
        
        #set a,b,c and d to the values extracted by the string key m and s
        a=self.numdic[str(m[0])]
        b=self.numdic[str(m[1])]
        c=self.numdic[str(s[0])]
        d=self.numdic[str(s[1])]

        #Change the time display on image by splitting the value by the comma, and changing the corresponding elements in the T*List to 0 (On state)
        for j in a.split(','):
            for row,column in TAList[int(j)-1]:
                image[row][column]=0

        for j in b.split(','):
            for row,column in TBList[int(j)-1]:
                image[row][column]=0

        
        for j in c.split(','):
            for row,column in TCList[int(j)-1]:
                image[row][column]=0
        
        for j in d.split(','):
            for row,column in TDList[int(j)-1]:
                image[row][column]=0


    def display(self):
        '''
        function that displays the 2d list of $image for 0.005 seconds. That way when put in a while loop there will be a good refresh rate. 
        '''

        #seconds=0.001
        #times=int(seconds*270)

        seconds=0.009
        times=int(seconds*270)

        #before= time.time()

        for times in range(times):
                for j in range(16):
                        GPIO.output(STB,0) 
                        for i in range(32):
                                GPIO.output(R1,int(image[j][i])) #[31-i]
                                GPIO.output(CLK,0)
                                GPIO.output(CLK,1)  
                                
                        #lights out (send 1 to output enable to block all LEDs)
                        GPIO.output(OE,1)  

                        GPIO.output(A, int(self.rowconv(j)[3]))
                        GPIO.output(B, int(self.rowconv(j)[2]))
                        GPIO.output(C, int(self.rowconv(j)[1]))
                        GPIO.output(D, int(self.rowconv(j)[0]))
                        
                        GPIO.output(STB,1)
                        #sends 0 to Output Enable so that LEDs are unblocked.
                        GPIO.output(OE,0)
                        
  
     

###################################### CONNECTION WITH THE DATABASE #########################


class Database:
    def __init__(self):
        '''
        Constructor of Database class: connects to the Database and resets some values
        '''


        global db,cursor
        #connects to the MySQL database
        db=MySQLdb.connect("localhost","tester","testing123","scoreboard")
        cursor=db.cursor()

        #clears the Timer table
        cursor.execute("DELETE FROM Timer")

        #clears the CurrentScore table
        cursor.execute("DELETE FROM CurrentScore")

        #sets the new score to 0:0 for both teams
        cursor.execute("INSERT INTO CurrentScore(shc,vis) VALUES(0,0)")


        #commit changes to the database
        db.commit()


    def FetchScore(self):
        '''
        To fetch the latest scores of both teams from the database and return them as an integer
        '''
        global score1,score2
        db=MySQLdb.connect("localhost","tester","testing123","scoreboard")
        cursor=db.cursor()
        cursor.execute("SELECT * FROM CurrentScore ORDER BY time DESC LIMIT 1")

        data=cursor.fetchone()

        return data[2],data[3]


######################## MAIN ROUTINE ######################################


if __name__=='__main__':

    #<GPIO SETUP>

    GPIO.setwarnings(False)
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
    #</GPIO SETUP>

    #initailise the object Matrix as an instance of class Matrix
    Matrix=Matrix() 

    #initialise the class Database
    Database=Database()

    #gets a start time
    start=time.time()

    while 1:
        #get the difference between time now and the start time
        #now is a large float
        now=time.time()-start

        #get the minute and seconds as the quotient and remainder when $now is divided by 60
        m, s = divmod(now, 60)

        #resets the Matrix to its initial state
        Matrix.reset()

        #Change the time on the display
        #m and s must be formatted to a 2 digit integer for ChangeTime
        Matrix.ChangeTime("%02i"%m,"%02i"%s)

        #fetch scores from the database, store them as score1 and score2
        score1,score2=Database.FetchScore()[0],Database.FetchScore()[1]

        #change the scores on the display
        Matrix.ChangeScore(score1,score2)

        Matrix.display()