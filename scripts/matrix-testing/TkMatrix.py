#!/usr/bin/python3
'''
This is a python Tkinter program to simulate a 16x32 LED Matrix
to enable the user to 'draw' on it and get the resulting data
in a list for displaying on a real LED matrix.

by Haoxi Tan
-the goal of this version is to also be able to output the result to a file and
so that i can be extracted by another program.
'''

#python 2/3 compatible
try:
    from tkinter import *
except:
    from Tkinter import *
import numpy as np

root=Tk()
root.title("TkMatrix")

#create the data matrix with numpy library
data=np.ones((16,32))


#create the output widget as a Label

display=Toplevel(root)
display.title("Display")
display.grid()


output=Text(display, font='Arial 10',width=60,height=25)
output.grid(row=16,column=0,columnspan=32)


#the function for toggling the values for the specific grid

def clear():
    global data
    data=np.ones((16,32))
    out=str(data)
    out=out.replace('.',',').replace(',]','],').replace(' ','').replace('\n',' ').replace('],','],\n').replace(' 1','1')

    output.delete(1.0,END)
    output.insert(END,out)
    mapbuttons()

def save(data):
    f=open('matrix','w')
    for i in data.tolist():
        l=len(i)
        print(str(i[0:l]).strip('[').strip(']').replace('.0',''))
        f.write(str(i[0:l]).strip('[').strip(']').replace('.0','')+'\n')
    f.close()

def load():
    f=open('matrix','r')
    data=[]
    for i in f:
        i=i.split(', ')
        data.append(i)
    f.close()
    print(data)
    #return data
    
def toggle(r,c):
    global data
    r,c=int(r),int(c)
    if data[r][c]==1:
        data[r][c]=0
    else:
        data[r][c]=1
    print('position:',str(r)+','+str(c),'New status:',int(data[r][c]))
    #string curation into a python list format
    out=str(data)
    out=out.replace('.',',').replace(',]','],').replace(' ','').replace('\n',' ').replace('],','],\n').replace(' 1','1') 

    output.delete(1.0,END)
    output.insert(END,out)
    #string curation into a python list format
    output.insert(END, ('\n\nLit coordinates:\n'+
                        str(np.argwhere(data == 0)).replace('\n',' ').replace('[ ','[').replace(']  [','],[').replace('  ',',').replace(' ',',') ))

    #print(data.tolist())

    

#use a nested loop based on the data matrix to draw all the buttons
def mapbuttons():
    global data

    for r in range(len(data)):
        for c in range(len(data[r])):
            #text=(str(r)+','+str(c)),
            buttons=Checkbutton(font='Arial 8',command=lambda r=r,c=c :toggle(r,c))
            buttons.grid(row=r,column=c)

clearbutton=Button(text='Clear',width=32,height=2,font='Arial 8',command=lambda:clear())
clearbutton.grid(row=16,column=0,columnspan=30,sticky=E)

savebutton=Button(text='Save',width=32,height=2,font='Arial 8',command=lambda:save(data))
savebutton.grid(row=16,column=0,columnspan=30,sticky=W)

loadbutton=Button(text='Load',width=32,height=2,font='Arial 8',command=lambda:load())
loadbutton.grid(row=16,column=0,columnspan=30)

mapbuttons()

if __name__=='__main__':
    root.mainloop()
    
