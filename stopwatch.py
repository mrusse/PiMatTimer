import tkinter as tk
import threading
from gpiozero import Button
from time import time
import random
import sys
import os
import logging

class Stopwatch:
    
    def __init__(self):

        self.root = tk.Tk()
        self.root.title('CubeTimer')
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none") 

        self.lastScramble = ""
        logging.basicConfig(filename="solves.txt",format='%(message)s',filemode='a')
        self.logger=logging.getLogger()  
        self.logger.setLevel(logging.DEBUG)  

        #timer label
        self.display = tk.Label(self.root, text='0.00', font = ("Arial Bold", 50))
        self.display.pack()
        self.display.place(relx = 0.5, rely = 0.5, anchor = 'center')

        #listbox and scrollbar
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.solvesList = tk.Listbox(self.root, height = 14, width = 58, yscrollcommand = self.scrollbar.set,font = ("Arial 11 bold")) 
        self.solvesList.pack(side= tk.LEFT, fill = tk.Y)
        self.scrollbar.config(command = self.solvesList.yview)
        self.scrollbar.pack_forget()
        self.solvesList.pack_forget()       
 
        #view solves button
        self.infoButton = tk.Button(self.root,text = 'View Solves',width= 40,font = ("Arial 12 bold"),command=self.view_solves)
        self.infoButton.pack()
        self.infoButton.place(relx = 0.5, rely = 0.92, anchor = 'center') 

        #back button
        self.backButton = tk.Button(self.root,text = 'Back',font = ("Arial 12 bold"),command=self.view_timer)
        self.backButton.pack()
        self.backButton.place(relx = 0.5, rely = 0.92, anchor = 'center') 
        self.backButton.place_forget()

        #get first scramble from file then delete it from the file
        stream = os.popen('head -n 1 scrambles.txt')
        scramblestr = stream.read() 
        os.system('tail -n +2 "scrambles.txt" > "tmp.txt" && mv "tmp.txt" "scrambles.txt"')       
        
        #scramble label
        #split scramble in half and put second half on new line to increase readability 
        middle = int(len(scramblestr)/2)

        if scramblestr[middle] == " ":
            scramblestr = scramblestr[:middle] +  "\n" + scramblestr[middle:]
        elif scramblestr[middle + 1] == " ":
            scramblestr = scramblestr[:middle + 1] +  "\n" + scramblestr[middle + 1:]
        else:
            scramblestr = scramblestr[:middle - 1] +  "\n" + scramblestr[middle -1 :]

        self.scramble = tk.Label(self.root, text= scramblestr, font = ("Arial 14 bold"))
        self.scramble.pack()
        self.scramble.place(relx = 0.5, rely = 0.13, anchor = 'center')

        #GPIO pins 19 and 26
        self.button1 = Button(19)
        self.button2 = Button(26)
 
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

                self.display.config(foreground = "red")
   
                lastTime = self.display.cget("text")
                self.toggle()

                #this appends to a log file lawl
                solveStr = lastTime + " - " + self.lastScramble.replace("\n", "") 
                self.logger.info(solveStr) 
                print(solveStr)

                self.solvesList.insert(0, ") " + lastTime) 
                self.solvesList.insert(1,self.lastScramble.replace("\n", ""))
                self.solvesList.insert(2," ")

                print(self.solvesList.size())

                if self.solvesList.size() > 13:
                    ao5Array = []
                    ao5Array.append(self.solvesList.get(0).split(") ")[1]) 
                    ao5Array.append(self.solvesList.get(3).split(") ")[1])
                    ao5Array.append(self.solvesList.get(6).split(") ")[1])
                    ao5Array.append(self.solvesList.get(9).split(") ")[1])
                    ao5Array.append(self.solvesList.get(12).split(") ")[1])

                    top = float(ao5Array[0])
                    bot = float(ao5Array[0])
                                        

                self.display.update_idletasks()

                self.scramble.place(relx = 0.5, rely = 0.13, anchor = 'center')
                self.infoButton.place(relx = 0.5, rely = 0.92, anchor = 'center') 

                os.system('tail -n +2 "scrambles.txt" > "tmp.txt" && mv "tmp.txt" "scrambles.txt"')       
 
                self.button1.wait_for_release()
                self.button2.wait_for_release()

                self.display.config(foreground = "black")

            else:
                self.display.config(foreground = "green")
                self.infoButton.place_forget() 
                self.scramble.place_forget()

                self.lastScramble = self.scramble.cget("text")
                self.display.update_idletasks() 

                self.button1.wait_for_release()
                self.button2.wait_for_release()

                stream = os.popen('head -n 1 scrambles.txt')
                scramblestr = stream.read()
              
                #split scramble in half and put second half on new line to increase readability 
                middle = int(len(scramblestr)/2)

                if scramblestr[middle] == " ":
                    scramblestr = scramblestr[:middle] +  "\n" + scramblestr[middle:]
                elif scramblestr[middle + 1] == " ":
                    scramblestr = scramblestr[:middle + 1] +  "\n" + scramblestr[middle + 1:]
                else:
                    scramblestr = scramblestr[:middle - 1] +  "\n" + scramblestr[middle -1 :]
 
                self.scramble.config(text = scramblestr)

                self.display.config(foreground = "black")
                self.toggle()

        self.display.after(10,self.checkInput)

    def view_solves(self):

        self.solvesList.pack(side = tk.LEFT,anchor = tk.NW,fill = tk.X)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.backButton.place(relx = 0.5, rely = 0.92, anchor = 'center')

        self.solvesList.delete(0,tk.END)

        solveFile = open("solves.txt")
        solveArray = []
    
        x = 1

        for line in solveFile:
            if x < 10:
                solveArray.append("  " + str(x) + ") " + str(line).strip())
            else:
                solveArray.append(str(x) + ") " + str(line).strip())
            x += 1
    
        solveArray.reverse()
    
        for i in range(len(solveArray)):
            current = solveArray[i].split(" - ")
            self.solvesList.insert(tk.END,current[0])
            self.solvesList.insert(tk.END,current[1])
            self.solvesList.insert(tk.END," ") 

        solveFile.close() 

        self.scramble.place_forget()
        self.infoButton.place_forget() 
        self.display.place_forget()

    def view_timer(self):
        self.scramble.place(relx = 0.5, rely = 0.13, anchor = 'center')
        self.infoButton.place(relx = 0.5, rely = 0.92, anchor = 'center') 
        self.display.place(relx = 0.5, rely = 0.5, anchor = 'center')

        self.backButton.place_forget()
        self.solvesList.pack_forget()
        self.scrollbar.pack_forget()
       
Stopwatch()
