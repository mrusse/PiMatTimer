import tkinter as tk
import threading
from gpiozero import Button
from time import time
import random
import sys
import os
import logging
import _thread
from subprocess import call
from pyTwistyScrambler.pyTwistyScrambler import scrambler333, scrambler222, scrambler444, scrambler555, scrambler666, scrambler777
#import imagegen as cubeimage

class Stopwatch:
    
    def __init__(self):

        self.root = tk.Tk()
        self.root.title('CubeTimer')
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none",bg = "#BFBFBF") 

        self.lastScramble = ""
        logging.basicConfig(filename="/home/pi/CubeTimer/solves.txt",format='%(message)s',filemode='a')
        self.logger=logging.getLogger()  
        self.logger.setLevel(logging.DEBUG)  

        #timer label
        self.display = tk.Label(self.root,bg = "#BFBFBF" ,text='0.00', font = ("Arial Bold", 50))
        self.display.place(relx = 0.5, rely = 0.48, anchor = 'center')
               
        #settings button 
        settingImage = tk.PhotoImage(file = "/home/pi/CubeTimer/settingsicon.gif")
        
        self.settingsButton= tk.Button(self.root,highlightthickness = 0,text = 'Back',image = settingImage,font = ("Arial 12 bold"),command=self.view_settings)
        self.settingsButton.place(relx = 0.09, rely = 0.92, anchor = 'center')

        #logo label
        logoImage = tk.PhotoImage(file = "/home/pi/CubeTimer/logo.gif")
        self.logo = tk.Label(self.root,bg = "#BFBFBF" ,image = logoImage)
        
        #cube dropdown
        self.cubeList = ["3x3x3", "2x2x2" , "4x4x4" , "5x5x5" , "6x6x6" , "7x7x7"]
        self.selectedCube = tk.StringVar(self.root)
        self.selectedCube.set("3x3x3")
 
        self.dropdownLabel = tk.Label(self.root,bg = "#BFBFBF" ,font = ("Arial 13 bold"),text = "Select puzzle type")

        self.cubeDropdown = tk.OptionMenu(self.root,self.selectedCube, *self.cubeList)

        #listbox and scrollbar
        self.scrollbar = tk.Scrollbar(self.root)
        self.solvesList = tk.Listbox(self.root, height = 14, width = 58, yscrollcommand = self.scrollbar.set,font = ("Arial 11 bold")) 
        self.scrollbar.config(command = self.solvesList.yview)       

        #ao5 label
        self.ao5Label = tk.Label(self.root, bg = "#BFBFBF",text='ao5: ', font = ("Arial 13 bold"))
        self.ao5Label.place(relx = 0.5, rely = 0.64, anchor = 'center')

        #ao12 label
        self.ao12Label = tk.Label(self.root,bg = "#BFBFBF" ,text='ao12: ', font = ("Arial 13 bold")) 
        self.ao12Label.place(relx = 0.5, rely = 0.72, anchor = 'center')
        
        #view solves button
        infoImage = tk.PhotoImage(file = "/home/pi/CubeTimer/infoicon.gif") 
        self.infoButton = tk.Button(self.root,image = infoImage,highlightthickness = 0,command=self.view_solves)
        self.infoButton.place(relx = 0.24, rely = 0.92, anchor = 'center') 

        #back button
        self.backButton = tk.Button(self.root,text = 'Back',font = ("Arial 12 bold"),command=self.view_timer)  
        
        #delete selected button
        self.removeSelected = tk.Button(self.root,text = 'Delete Selected Time',font = ("Arial 12 bold"),command=self.remove_selected)  
        
        #exit button
        self.exit = tk.Button(self.root,text = 'Exit',font = ("Arial 12 bold"),command=self.exit)  

        #shutdown button
        self.shutdown = tk.Button(self.root,text = 'Shutdown',font = ("Arial 12 bold"),command=self.shutdown)  

        #get first scramble from file then delete it from the file then generate new scramble in a new thread
        stream = os.popen('head -n 1 /home/pi/CubeTimer/scrambles333.txt')
        scramblestr = stream.read() 
        os.system('tail -n +2 "/home/pi/CubeTimer/scrambles333.txt" > "/home/pi/CubeTimer/tmp.txt" && mv "/home/pi/CubeTimer/tmp.txt" "/home/pi/CubeTimer/scrambles333.txt"')       
        _thread.start_new_thread(self.scramble3,())
        
        
        #scrambleimage label

        command = "python3 /home/pi/CubeTimer/imagegen.py" + " \"" + scramblestr + "\""
        os.system(command)        

        self.scramblePic = tk.PhotoImage(file = "/home/pi/CubeTimer/cubelarge.gif")
        #os.remove("cubeimage.gif")
        self.scrambleImage = tk.Label(self.root,bg = "#BFBFBF" ,image = self.scramblePic)
        self.scrambleImage.place(relx = 0.97, rely = 0.97, anchor = tk.SE)
    
      
        #fill up listbox and get average
        if os.path.isfile("/home/pi/CubeTimer/solves.txt"):
            solveFile = open("/home/pi/CubeTimer/solves.txt")
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

            self.set_average(5) 
            self.set_average(12)            
    
        #scramble label
        #split scramble in half and put second half on new line to increase readability 
        middle = int(len(scramblestr)/2)

        if scramblestr[middle] == " ":
            scramblestr = scramblestr[:middle] +  "\n" + scramblestr[middle:]
        elif scramblestr[middle + 1] == " ":
            scramblestr = scramblestr[:middle + 1] +  "\n" + scramblestr[middle + 1:]
        else:
            scramblestr = scramblestr[:middle - 1] +  "\n" + scramblestr[middle -1 :]

        self.scramble = tk.Label(self.root,bg = "#BFBFBF", text= scramblestr, font = ("Arial 14 bold")) 
        self.scramble.place(relx = 0.5, rely = 0.13, anchor = 'center')

        #GPIO pins 19 and 26
        self.button1 = Button(19)
        self.button2 = Button(26)
        
        self.delta = 0
        self.paused = True

        self.check_input()  
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
        
        self.delta = (time() - self.oldtime)
        secstr = '%.2f' % self.delta
        minstr = int(self.delta /60)
        hourstr = int(minstr/60)
        
        if(minstr > 0):
            secstr = '%.2f' % (self.delta - (minstr * 60))
            if self.delta - (minstr * 60) < 10:
                self.display.config(text= str(minstr) + ":0" + secstr)
            else:
                self.display.config(text= str(minstr) + ":" + secstr)
        else:
            self.display.config(text=secstr)
        
        self.display.after(10, self.run_timer)

    def check_input(self):

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

                #print(self.solvesList.size())

                self.set_average(5)                                  
                self.set_average(12)

                self.display.update_idletasks()

                scramblestr = self.scramble.cget("text").replace("\n","")

                self.scrambleImage.destroy()
             
                try: 

                    with open("/home/pi/CubeTimer/cubelarge.gif", "rb") as last:
                        linelist = last.readlines()
                        last = linelist[len(linelist)-1].decode('ascii').replace("\n","")
                        print("image scramble: " + str(last) + "\n current scramble: " + scramblestr) 

                    if last == scramblestr:
                        self.scramblePic = tk.PhotoImage(file = "/home/pi/CubeTimer/cubelarge.gif")
                    else:
                        self.scramblePic = tk.PhotoImage(file = "/home/pi/CubeTimer/empty.gif")   
                    self.scrambleImage = tk.Label(self.root,bg = "#BFBFBF" ,image = self.scramblePic)
                    if self.selectedCube.get() == "3x3x3":
                        self.scrambleImage.place(relx = 0.97, rely = 0.97, anchor = tk.SE)
                except:
                    self.scramblePic = tk.PhotoImage(file = "/home/pi/CubeTimer/empty.gif")
                    self.scrambleImage = tk.Label(self.root,bg = "#BFBFBF" ,image = self.scramblePic)
                    if self.selectedCube.get() == "3x3x3":
                        self.scrambleImage.place(relx = 0.97, rely = 0.97, anchor = tk.SE)

                    print("----------stop spamming so hard mitch----------")
   
                self.ao5Label.place(relx = 0.5, rely = 0.64, anchor = 'center')
                self.ao12Label.place(relx = 0.5, rely = 0.72, anchor = 'center') 
                self.infoButton.place(relx = 0.24, rely = 0.92, anchor = 'center') 
                self.settingsButton.place(relx = 0.09, rely = 0.92, anchor = 'center') 
                
                if self.selectedCube.get() == "4x4x4" or self.selectedCube.get() == "5x5x5": 
                    self.scramble.place(relx = 0.5, rely = 0.16, anchor = 'center')
                if self.selectedCube.get() == "3x3x3" or self.selectedCube.get() == "2x2x2":
                    self.scramble.place(relx = 0.5, rely = 0.13, anchor = 'center')       
                if self.selectedCube.get() == "7x7x7":
                    self.scramble.place(relx = 0.5, rely = 0.18, anchor = 'center')      
                self.button1.wait_for_release()
                self.button2.wait_for_release() 
                
                self.display.config(foreground = "black")

            else:
                self.display.config(foreground = "green")
                self.infoButton.place_forget() 
                self.scramble.place_forget()
                self.ao5Label.place_forget()
                self.ao12Label.place_forget()
                self.settingsButton.place_forget()
                self.scrambleImage.place_forget()
                #self.scramblePic = tk.PhotoImage(file = "/home/pi/CubeTimer/empty.gif")   
 
                self.lastScramble = self.scramble.cget("text")
                self.display.update_idletasks() 

                self.button1.wait_for_release()
                self.button2.wait_for_release()

                self.get_scramble(True)
                self.display.config(foreground = "black")
                self.toggle()
                #self.scramblePic = tk.PhotoImage(file = "/home/pi/CubeTimer/empty.gif")   
 

        self.display.after(10,self.check_input)

    def view_solves(self):

        self.solvesList.pack(side = tk.LEFT,anchor = tk.NW,fill = tk.X)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.backButton.place(relx = 0.2, rely = 0.92, anchor = 'center')
        self.removeSelected.place(relx = 0.65, rely = 0.92, anchor = 'center') 
        
        self.solvesList.delete(0,tk.END)

        if os.path.isfile("/home/pi/CubeTimer/solves.txt"):
            solveFile = open("/home/pi/CubeTimer/solves.txt")
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
        
        self.ao5Label.place_forget()
        self.ao12Label.place_forget()
        self.scramble.place_forget()
        self.infoButton.place_forget() 
        self.display.place_forget()
        self.settingsButton.place_forget()
        self.scrambleImage.place_forget()

    def view_timer(self):
        if self.selectedCube.get() == "4x4x4" or self.selectedCube.get() == "5x5x5": 
            self.scramble.place(relx = 0.5, rely = 0.16, anchor = 'center')
        if self.selectedCube.get() == "7x7x7":
            self.scramble.place(relx = 0.5, rely = 0.18, anchor = 'center')
        if self.selectedCube.get() == "3x3x3" or self.selectedCube.get() == "2x2x2":
            self.scramble.place(relx = 0.5, rely = 0.13, anchor = 'center')
        self.infoButton.place(relx = 0.25, rely = 0.92, anchor = 'center') 
        self.display.place(relx = 0.5, rely = 0.48, anchor = 'center')
        self.ao5Label.place(relx = 0.5, rely = 0.64, anchor = 'center')
        self.ao12Label.place(relx = 0.5, rely = 0.72, anchor = 'center')
        self.settingsButton.place(relx = 0.08, rely = 0.92, anchor = 'center')
        self.scrambleImage.place(relx = 0.97, rely = 0.97, anchor = tk.SE)
    

        if self.logo.winfo_ismapped():
            self.get_scramble(False)

            if self.selectedCube.get() == "3x3x3":
                solvestr = self.scramble.cget("text").replace("\n","")

                command = "python3 /home/pi/CubeTimer/imagegen.py" + " \"" + solvestr  + "\""
                os.system(command)
                self.scrambleImage.destroy()

                self.scramblePic = tk.PhotoImage(file = "/home/pi/CubeTimer/cubelarge.gif")
                #os.remove("cubeimage.gif")
                self.scrambleImage = tk.Label(self.root,bg = "#BFBFBF" ,image = self.scramblePic)
                self.scrambleImage.place(relx = 0.97, rely = 0.97, anchor = tk.SE)
            else:
                self.scrambleImage.place_forget()     
            print(self.selectedCube.get())

        self.backButton.place_forget()
        self.solvesList.pack_forget()
        self.scrollbar.pack_forget()
        self.removeSelected.place_forget()
        self.exit.place_forget()
        self.shutdown.place_forget()
        self.cubeDropdown.place_forget()
        self.logo.place_forget()
        self.dropdownLabel.place_forget()
 
    def view_settings(self):
        self.exit.place(relx = 0.48, rely = 0.92, anchor = 'center') 
        self.shutdown.place(relx = 0.71, rely = 0.92, anchor = 'center')
        self.backButton.place(relx = 0.28, rely = 0.92, anchor = 'center')
        self.cubeDropdown.place(relx = 0.69, rely = 0.38, anchor = 'center')
        self.logo.place(relx = 0.3, rely = 0.4, anchor = 'center')
        self.dropdownLabel.place(relx = 0.76, rely = 0.24, anchor = 'center')

        self.ao5Label.place_forget()
        self.ao12Label.place_forget()
        self.scramble.place_forget()
        self.infoButton.place_forget() 
        self.display.place_forget()
        self.settingsButton.place_forget()
        self.scrambleImage.place_forget()

    def remove_selected(self):
        
        selection = self.solvesList.curselection()
        selectedArray = self.solvesList.get(selection[0]).split(") ") 

        if not (len(selectedArray) > 1):
            return

        if ":" in selectedArray[1]:
            selectedArray[1].replace(':','')
            
        #if isinstance(float(selectedArray[1].rstrip()),float):
        self.solvesList.delete(selection[0],selection[0]+2)
            
        lineToDelete = selectedArray[0].strip()
        deleteString = "sed -i '{0}d' /home/pi/CubeTimer/solves.txt".format(lineToDelete)
        os.system(deleteString)
        print("Deleted solve #" + lineToDelete + ": " +selectedArray[1])

        self.set_average(5)
        self.set_average(12)
        self.view_solves()
        self.solvesList.see(selection[0])

    
    def set_average(self, number):
        
        if self.solvesList.size() >= ((number*3) - 1):

            aoArray = []

            for i in range(0,number*3,3):
                if ":" in self.solvesList.get(i).split(") ")[1]:
                    minute = self.solvesList.get(i).split(") ")[1].split(":")
                    secondsToAdd = float(float(minute[0]) * 60)
                    aoArray.append(float(float(minute[1]) + secondsToAdd))
                else:
                    aoArray.append(float(self.solvesList.get(i).split(") ")[1])) 
                                               
            #for k in range(number):
                #print(aoArray[k])                
 
            top = aoArray[0]
            bot = aoArray[0]
            total = 0

            #print(len(aoArray))
                    
            for j in range(number):
                if aoArray[j] > top:
                    top = aoArray[j]
                if aoArray[j] < bot:
                    bot = aoArray[j]
                    
            for j in range(number):
                if not aoArray[j] == top and not aoArray[j] == bot:
                    total += aoArray[j]
                    
            average = '%.2f' % (total / (number - 2))
            if number == 5:
                self.ao5Label.config(text= "ao5: " + str(average)) 
            if number == 12:
                self.ao12Label.config(text= "ao12: " + str(average)) 
        else:
            if number == 5:
                self.ao5Label.config(text= "ao5: ") 
            if number == 12:
                self.ao12Label.config(text= "ao12: ") 

    def get_scramble(self,getImage):

        if self.selectedCube.get() == "3x3x3":
            stream = os.popen('head -n 1 /home/pi/CubeTimer/scrambles333.txt')
            os.system('tail -n +2 "/home/pi/CubeTimer/scrambles333.txt" > "/home/pi/CubeTimer/tmp.txt" && mv "/home/pi/CubeTimer/tmp.txt" "/home/pi/CubeTimer/scrambles333.txt"')       
            _thread.start_new_thread(self.scramble3, ())
            scramblestr = stream.read()

#            if os.path.exists("/home/pi/CubeTimer/cube.gif"):
 #               os.remove("/home/pi/CubeTimer/cube.gif")
 
            if getImage:
                command = "python3 /home/pi/CubeTimer/imagegen.py" + " \"" + scramblestr + "\""
                _thread.start_new_thread(os.system,(command,))        
 

            #split scramble in half and put second half on new line to increase readability 
            middle = int(len(scramblestr)/2)

            if scramblestr[middle] == " ":
                scramblestr = scramblestr[:middle] +  "\n" + scramblestr[middle:]
            elif scramblestr[middle + 1] == " ":
                scramblestr = scramblestr[:middle + 1] +  "\n" + scramblestr[middle + 1:]
            else:
                scramblestr = scramblestr[:middle - 1] +  "\n" + scramblestr[middle -1 :]
 
            self.scramble.config(text = scramblestr,font = ("Arial 14 bold"))

        if self.selectedCube.get() == "4x4x4":
            stream = os.popen('head -n 1 /home/pi/CubeTimer/scrambles444.txt')
            os.system('tail -n +2 "/home/pi/CubeTimer/scrambles444.txt" > "/home/pi/CubeTimer/tmp.txt" && mv "/home/pi/CubeTimer/tmp.txt" "/home/pi/CubeTimer/scrambles444.txt"')       
            _thread.start_new_thread(self.scramble4, ())
            scramblestr = stream.read()
            print(scramblestr)  
            #split scramble in thirds 
            third = int(len(scramblestr)/3)

            #first third
            if scramblestr[third] == " ":
                scramblestr = scramblestr[:third] +  "\n" + scramblestr[third:]
            elif scramblestr[third + 1] == " ":
                scramblestr = scramblestr[:third + 1] +  "\n" + scramblestr[third + 1:]
            elif scramblestr[third - 1] == " ":
                scramblestr = scramblestr[:third - 1] +  "\n" + scramblestr[third - 1:]
            elif scramblestr[third + 2] == " ":
                scramblestr = scramblestr[:third + 2] +  "\n" + scramblestr[third + 2:]
            else:
                scramblestr = scramblestr[:third - 2] +  "\n" + scramblestr[third - 2:]
            
            #last third
            if scramblestr[third*2] == " ":
                scramblestr = scramblestr[:third*2] +  "\n" + scramblestr[third*2:]
            elif scramblestr[third*2 + 1] == " ":
                scramblestr = scramblestr[:third*2 + 1] +  "\n" + scramblestr[third*2 + 1:]
            elif scramblestr[third*2 - 1] == " ":
                scramblestr = scramblestr[:third*2 - 1] +  "\n" + scramblestr[third*2 -1 :]
            elif scramblestr[third*2 + 2] == " ":
                scramblestr = scramblestr[:third*2 + 2] +  "\n" + scramblestr[third*2 + 2:]
            else:
                scramblestr = scramblestr[:third*2 - 2] +  "\n" + scramblestr[third*2 - 2:]            
           
            print(scramblestr)  
            self.scramble.config(text = scramblestr,font = ("Arial 14 bold"))

        if self.selectedCube.get() == "2x2x2":
            stream = os.popen('head -n 1 /home/pi/CubeTimer/scrambles222.txt')
            os.system('tail -n +2 "/home/pi/CubeTimer/scrambles222.txt" > "/home/pi/CubeTimer/tmp.txt" && mv "/home/pi/CubeTimer/tmp.txt" "/home/pi/CubeTimer/scrambles222.txt"')       
            _thread.start_new_thread(self.scramble2, ())
            scramblestr = stream.read()
            self.scramble.config(text = scramblestr,font = ("Arial 14 bold"))
        
        if self.selectedCube.get() == "5x5x5":
            stream = os.popen('head -n 1 /home/pi/CubeTimer/scrambles555.txt')
            os.system('tail -n +2 "/home/pi/CubeTimer/scrambles555.txt" > "/home/pi/CubeTimer/tmp.txt" && mv "/home/pi/CubeTimer/tmp.txt" "/home/pi/CubeTimer/scrambles555.txt"')       
            _thread.start_new_thread(self.scramble5, ())
            scramblestr = stream.read()
            print(scramblestr)  
            #split scramble in thirds 
            third = int(len(scramblestr)/4)

            #first third
            if scramblestr[third] == " ":
                scramblestr = scramblestr[:third] +  "\n" + scramblestr[third:]
            elif scramblestr[third + 1] == " ":
                scramblestr = scramblestr[:third + 1] +  "\n" + scramblestr[third + 1:]
            elif scramblestr[third - 1] == " ":
                scramblestr = scramblestr[:third - 1] +  "\n" + scramblestr[third - 1:]
            elif scramblestr[third + 2] == " ":
                scramblestr = scramblestr[:third + 2] +  "\n" + scramblestr[third + 2:]
            else:
                scramblestr = scramblestr[:third - 2] +  "\n" + scramblestr[third - 2:]
            
            #last third
            if scramblestr[third*2] == " ":
                scramblestr = scramblestr[:third*2] +  "\n" + scramblestr[third*2:]
            elif scramblestr[third*2 + 1] == " ":
                scramblestr = scramblestr[:third*2 + 1] +  "\n" + scramblestr[third*2 + 1:]
            elif scramblestr[third*2 - 1] == " ":
                scramblestr = scramblestr[:third*2 - 1] +  "\n" + scramblestr[third*2 -1 :]
            elif scramblestr[third*2 + 2] == " ":
                scramblestr = scramblestr[:third*2 + 2] +  "\n" + scramblestr[third*2 + 2:]
            else:
                scramblestr = scramblestr[:third*2 - 2] +  "\n" + scramblestr[third*2 - 2:]            
            
            #last third
            if scramblestr[third*3] == " ":
                scramblestr = scramblestr[:third*3] +  "\n" + scramblestr[third*3:]
            elif scramblestr[third*3 + 1] == " ":
                scramblestr = scramblestr[:third*3 + 1] +  "\n" + scramblestr[third*3 + 1:]
            elif scramblestr[third*3 - 1] == " ":
                scramblestr = scramblestr[:third*3 - 1] +  "\n" + scramblestr[third*3 -1 :]
            elif scramblestr[third*3 + 2] == " ":
                scramblestr = scramblestr[:third*3 + 2] +  "\n" + scramblestr[third*3 + 2:]
            else:
                scramblestr = scramblestr[:third*3 - 2] +  "\n" + scramblestr[third*3 - 2:]            
            


            print(scramblestr)  
            self.scramble.config(text = scramblestr,font = ("Arial 12 bold"))
    
        if self.selectedCube.get() == "7x7x7":
            stream = os.popen('head -n 1 /home/pi/CubeTimer/scrambles777.txt')
            os.system('tail -n +2 "/home/pi/CubeTimer/scrambles777.txt" > "/home/pi/CubeTimer/tmp.txt" && mv "/home/pi/CubeTimer/tmp.txt" "/home/pi/CubeTimer/scrambles777.txt"')       
            _thread.start_new_thread(self.scramble5, ())
            scramblestr = stream.read()
            print(scramblestr)  
            #split scramble in thirds 
            third = int(len(scramblestr)/6)

            #first third
            if scramblestr[third] == " ":
                scramblestr = scramblestr[:third] +  "\n" + scramblestr[third:]
            elif scramblestr[third + 1] == " ":
                scramblestr = scramblestr[:third + 1] +  "\n" + scramblestr[third + 1:]
            elif scramblestr[third - 1] == " ":
                scramblestr = scramblestr[:third - 1] +  "\n" + scramblestr[third - 1:]
            elif scramblestr[third + 2] == " ":
                scramblestr = scramblestr[:third + 2] +  "\n" + scramblestr[third + 2:]
            else:
                scramblestr = scramblestr[:third - 2] +  "\n" + scramblestr[third - 2:]
            
            #last third
            if scramblestr[third*2] == " ":
                scramblestr = scramblestr[:third*2] +  "\n" + scramblestr[third*2:]
            elif scramblestr[third*2 + 1] == " ":
                scramblestr = scramblestr[:third*2 + 1] +  "\n" + scramblestr[third*2 + 1:]
            elif scramblestr[third*2 - 1] == " ":
                scramblestr = scramblestr[:third*2 - 1] +  "\n" + scramblestr[third*2 -1 :]
            elif scramblestr[third*2 + 2] == " ":
                scramblestr = scramblestr[:third*2 + 2] +  "\n" + scramblestr[third*2 + 2:]
            else:
                scramblestr = scramblestr[:third*2 - 2] +  "\n" + scramblestr[third*2 - 2:]            
            
            #last third
            if scramblestr[third*3] == " ":
                scramblestr = scramblestr[:third*3] +  "\n" + scramblestr[third*3:]
            elif scramblestr[third*3 + 1] == " ":
                scramblestr = scramblestr[:third*3 + 1] +  "\n" + scramblestr[third*3 + 1:]
            elif scramblestr[third*3 - 1] == " ":
                scramblestr = scramblestr[:third*3 - 1] +  "\n" + scramblestr[third*3 -1 :]
            elif scramblestr[third*3 + 2] == " ":
                scramblestr = scramblestr[:third*3 + 2] +  "\n" + scramblestr[third*3 + 2:]
            else:
                scramblestr = scramblestr[:third*3 - 2] +  "\n" + scramblestr[third*3 - 2:]            
            
            #last third
            if scramblestr[third*4] == " ":
                scramblestr = scramblestr[:third*4] +  "\n" + scramblestr[third*4:]
            elif scramblestr[third*4 + 1] == " ":
                scramblestr = scramblestr[:third*4 + 1] +  "\n" + scramblestr[third*4 + 1:]
            elif scramblestr[third*4 - 1] == " ":
                scramblestr = scramblestr[:third*4 - 1] +  "\n" + scramblestr[third*4 -1 :]
            elif scramblestr[third*4 + 2] == " ":
                scramblestr = scramblestr[:third*4 + 2] +  "\n" + scramblestr[third*4 + 2:]
            else:
                scramblestr = scramblestr[:third*4 - 2] +  "\n" + scramblestr[third*4 - 2:]            
           
            #last third
            if scramblestr[third*5] == " ":
                scramblestr = scramblestr[:third*5] +  "\n" + scramblestr[third*5:]
            elif scramblestr[third*5 + 1] == " ":
                scramblestr = scramblestr[:third*5 + 1] +  "\n" + scramblestr[third*5 + 1:]
            elif scramblestr[third*5 - 1] == " ":
                scramblestr = scramblestr[:third*5 - 1] +  "\n" + scramblestr[third*5 -1 :]
            elif scramblestr[third*5 + 2] == " ":
                scramblestr = scramblestr[:third*5 + 2] +  "\n" + scramblestr[third*5 + 2:]
            else:
                scramblestr = scramblestr[:third*5 - 2] +  "\n" + scramblestr[third*5 - 2:]            
            

 
            print(scramblestr)  
            self.scramble.config(text = scramblestr,font = ("Arial 10 bold"))


    def scramble3(self):

        with open("/home/pi/CubeTimer/scrambles333.txt","a") as scrambleFile:
            print("Generating new 3x3 scramble")
            scrambleFile.write(scrambler333.get_WCA_scramble() + os.linesep)
            print("Generation complete")
    
    def scramble4(self):
        with open("/home/pi/CubeTimer/scrambles444.txt","a") as scrambleFile:
            print("Generating new 4x4 scramble")
            scrambleFile.write(scrambler444.get_WCA_scramble() + os.linesep)
            print("Generation complete")                                                                                
   
    def scramble2(self):
        with open("/home/pi/CubeTimer/scrambles222.txt","a") as scrambleFile:
            print("Generating new 2x2 scramble")
            scrambleFile.write(scrambler222.get_WCA_scramble() + os.linesep)
            print("Generation complete")

    def scramble5(self):
        with open("/home/pi/CubeTimer/scrambles555.txt","a") as scrambleFile:
            print("Generating new 5x5 scramble")
            scrambleFile.write(scrambler555.get_WCA_scramble() + os.linesep)
            print("Generation complete")
    
    def scramble7(self):
        with open("/home/pi/CubeTimer/scrambles777.txt","a") as scrambleFile:
            print("Generating new 7x7 scramble")
            scrambleFile.write(scrambler777.get_WCA_scramble() + os.linesep)
            print("Generation complete")



    def exit(self):
        quit()

    def shutdown(self):
        call("sudo nohup shutdown -h now", shell=True)
 
Stopwatch()
