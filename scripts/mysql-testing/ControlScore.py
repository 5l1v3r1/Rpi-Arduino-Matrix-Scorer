#!/usr/bin/python
#A script for inputting new scores into the database.

import MySQLdb

print "Welcome to score control! Enter a new score or enter e to quit."

db=MySQLdb.connect("localhost","tester","testing123","scoreboard") #makes connection with database
cursor=db.cursor()


shc=0 #SHC
vis=0 #visitor

def scoreconvIn(score):
    global shc,vis
    #this function converts the score into 2 numbers 
    try:
        score=score.split(':')
        shc=int(score[0])
        vis=int(score[1])
    except:
        print "Error while converting."

def reset():
    cursor.execute("insert into CurrentScore(time,shc,vis) values(localtime,0,0)")
    print cursor.fetchone()
        


newscore="0:0"

while 1:
    newscore=raw_input("Enter a new score: ")
    if newscore=='reset':
        reset()
    elif newscore=='exit' or newscore=='e':
        break
    scoreconvIn(newscore)
    print "SHC:%i VIS:%i" % (shc,vis)
    cursor.execute("insert into CurrentScore(time,shc,vis) values(localtime,%i,%i)"%(shc,vis))
    db.commit()

    
print "Exitted cleanly."
db.close()
