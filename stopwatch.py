import tkinter as tk
import threading
from gpiozero import Button
from time import time
import random
import sys
import os

#solves = open('solves.txt', 'a')

class Stopwatch:
    
    def __init__(self):

        self.root = tk.Tk()
        self.root.title('CubeTimer')
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none") 

        self.lastScramble = ""
        #self.solves = open('solves.txt', 'a',536870912)
     
        self.display = tk.Label(self.root, text='0.00', font = ("Arial Bold", 50))
        self.display.pack()
        self.display.place(relx = 0.5, rely = 0.5, anchor = 'center')

        self.infoButton = tk.Button(self.root,text = 'Session Info',width= 40,font = ("Arial 12 bold"),command=self.save)
        self.infoButton.pack()
        self.infoButton.place(relx = 0.5, rely = 0.92, anchor = 'center') 

        #get first scramble from file then delete it from the file
        stream = os.popen('head -n 1 scrambles.txt')
        scramblestr = stream.read() 
        stream = os.popen('sed "1d" -i\'\' scrambles.txt')       
        
        self.scramble = tk.Label(self.root, text= scramblestr, font = ("Arial 12 bold"))
        self.scramble.pack()
        self.scramble.place(relx = 0.5, rely = 0.1, anchor = 'center')

        #GPIO pins 19 and 26
        self.button1 = Button(19)
        self.button2 = Button(26)

        #self.close()
        self.paused = True

        self.checkInput()  
        self.root.mainloop()
        

    #toggle the timer on and off
    def toggle(self):
        
        if self.paused:
            self.paused = False
            self.oldtime = time()
            self.run_timer()
        else:
            self.paused = True
            self.oldtime = time()

    #timer that updates the label
    def run_timer(self):
        
        if self.paused:
            return
        
        delta = (time() - self.oldtime)
        secstr = '%.2f' % delta
        minstr = int(delta /60)
        hourstr = int(minstr/60)
        
        if(minstr > 0):
            secstr = '%.2f' % (delta - (minstr * 60))
            if delta - (minstr * 60) < 10:
                self.display.config(text= str(minstr) + ":0" + secstr)
            else:
                self.display.config(text= str(minstr) + ":" + secstr)
        else:
            self.display.config(text=secstr)
        
        self.display.after(10, self.run_timer)

    def checkInput(self):


        if self.button1.is_pressed and self.button2.is_pressed:

            if not self.paused:                
   
                lastTime = self.display.cget("text")
                self.toggle()

                #this appends to a log file lawl
                solveStr = lastTime + " - " + self.lastScramble 
                print(solveStr)

                self.display.update_idletasks()

                self.scramble.place(relx = 0.5, rely = 0.1, anchor = 'center')
                self.infoButton.place(relx = 0.5, rely = 0.92, anchor = 'center') 

                self.button1.wait_for_release()
                self.button2.wait_for_release()

            else:
                self.display.config(foreground = "green")
                self.infoButton.place(relx = 0.5, rely = 2, anchor = 'center') 
                self.scramble.place(relx = 0.5, rely = -1, anchor = 'center')

                self.lastScramble = self.scramble.cget("text")
                self.display.update_idletasks() 

                self.button1.wait_for_release()
                self.button2.wait_for_release()

                stream = os.popen('head -n 1 scrambles.txt')
                scramblestr = stream.read()
                stream = os.popen('sed "1d" -i\'\' scrambles.txt')
                self.scramble.config(text = scramblestr)

                self.display.config(foreground = "black")
                self.toggle()

        self.display.after(10,self.checkInput)

    def save(self):
        print("here")
        quit()
        #solves.flush()
       

  

Stopwatch()
