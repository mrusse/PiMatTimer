import tkinter as tk
from gpiozero import Button
from time import time
import random
import sys
import os
import logging
import platform
import _thread
from subprocess import call
from pyTwistyScrambler.pyTwistyScrambler import scrambler333, scrambler222, scrambler444, scrambler555, scrambler666, scrambler777
import socket
from termcolor import colored

class Stopwatch:
    
    def __init__(self):

        self.root = tk.Tk()
        self.root.title('PiMatTimer')
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none",bg = "#BFBFBF") 

        self.inspectionReady = False
        self.lastScramble = ""
        self.system = platform.system()
   
        if os.path.isdir("/home/pi/PiMatTimer/"):
            self.path = "/home/pi/PiMatTimer/"
            self.resources = self.path + "resources/"
            self.solvepath = self.path + "solves/"
        else:
            
            if self.system == "Windows":
                self.path ="\\"
                self.resources = self.path + "resources\\"
                self.solvepath = self.path + "solves\\"
            else:
                self.path = "/"
                self.resources = self.path + "resources/"
                self.solvepath = self.path + "solves/"
        
        #try to connect to webserver, single retry
        self.ipLabel = "" 
        self.connectionAttempt = False
        self.connect_webserver(True)        

        #timer label
        self.display = tk.Label(self.root,bg = "#BFBFBF" ,text='0.00', font = ("Arial Bold", 50))
        self.display.place(relx = 0.5, rely = 0.48, anchor = 'center')
               
        #settings button 
        settingImage = tk.PhotoImage(file = self.resources + "settingsicon.gif")
        
        self.settingsButton= tk.Button(self.root,highlightthickness = 0,text = 'Back',image = settingImage,font = ("Arial 12 bold"),command=self.view_settings)
        self.settingsButton.place(relx = 0.09, rely = 0.92, anchor = 'center')

        #logo label
        logoImage = tk.PhotoImage(file = self.resources + "logo.gif")
        self.logo = tk.Label(self.root,bg = "#BFBFBF" ,image = logoImage)
        
        #divider label
        barImage = tk.PhotoImage(file = self.resources + "bar.gif")
        self.bar = tk.Label(self.root,bg = "#BFBFBF" ,image = barImage)
               
        #cube dropdown
        self.cubeList = ["3x3x3", "2x2x2" , "4x4x4" , "5x5x5" , "6x6x6" , "7x7x7"]
        self.selectedCube = tk.StringVar(self.root)
        self.selectedCube.set("3x3x3")
        self.lastSelectedCube = "3x3x3"
 
        self.dropdownLabel = tk.Label(self.root,bg = "#BFBFBF" ,font = ("Arial 13 bold"),text = "Select puzzle type")

        self.cubeDropdown = tk.OptionMenu(self.root,self.selectedCube, *self.cubeList)

        #inspection dropdown
        self.inspectionList = ["No ", "Yes"]
        self.selectedInspection = tk.StringVar(self.root)
        self.selectedInspection.set("No ")
 
        self.inspectionLabel = tk.Label(self.root,bg = "#BFBFBF" ,font = ("Arial 13 bold"),text = "Use WCA Inspection")

        self.inspectionDropdown = tk.OptionMenu(self.root,self.selectedInspection, *self.inspectionList)

        if os.path.isfile(self.resources + "settings.txt"):
            with open(self.resources + "settings.txt") as settingsFile:
                options = settingsFile.readlines()
                self.selectedCube.set(options[0].strip())
                self.selectedInspection.set(options[1].strip())

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
        infoImage = tk.PhotoImage(file = self.resources + "infoicon.gif") 
        self.infoButton = tk.Button(self.root,image = infoImage,highlightthickness = 0,command=self.view_solves)
        self.infoButton.place(relx = 0.24, rely = 0.92, anchor = 'center') 

        #back button
        self.backButton = tk.Button(self.root,text = 'Back',font = ("Arial 12 bold"),command=self.view_timer)  
        
        #delete selected button
        self.removeSelected = tk.Button(self.root,text = 'Delete Selected Time',font = ("Arial 12 bold"),command=self.remove_selected)  
        
        #exit button
        self.exit = tk.Button(self.root,text = 'Exit',font = ("Arial 12 bold"),command=self.exit)  

        #sleep button
        self.sleepButton = tk.Button(self.root,text = 'Sleep',font = ("Arial 12 bold"),command=self.sleep_display)  


        #shutdown button
        self.shutdown = tk.Button(self.root,text = 'Shutdown',font = ("Arial 12 bold"),fg='#F80000',command=self.shutdown)  

        #get first scramble from file then delete it from the file then generate new scramble in a new thread
        self.scramble = tk.Label(self.root,bg = "#BFBFBF", text= "", font = ("Arial 15 bold")) 
        if self.selectedCube.get() == "4x4x4" or self.selectedCube.get() == "5x5x5": 
            self.scramble.place(relx = 0.5, rely = 0.16, anchor = 'center')
        if self.selectedCube.get() == "7x7x7" or self.selectedCube.get() == "6x6x6":
            self.scramble.place(relx = 0.5, rely = 0.2, anchor = 'center')
        if self.selectedCube.get() == "3x3x3" or self.selectedCube.get() == "2x2x2":
            self.scramble.place(relx = 0.5, rely = 0.13, anchor = 'center')
       
        if self.selectedCube.get() == "3x3x3": 
            #get first scramble from file then delete it from the file then generate new scramble in a new thread
            stream = os.popen('head -n 1 ' + self.resources + 'scrambles333.txt')
            scramblestr = stream.read() 
            os.system('tail -n +2 "' + self.resources + 'scrambles333.txt" > "' + self.resources + 'tmp.txt" && mv "' + self.resources + 'tmp.txt" "' + self.resources + 'scrambles333.txt"')       
            _thread.start_new_thread(self.scramble3,())
        
        
            #scrambleimage label

            command = 'python3 ' + self.path + 'imagegen.py' + ' \"' + scramblestr + '\"'
            os.system(command)    

            scramblestr = self.split_scramble(scramblestr,2) 
            self.scramble.config(text = scramblestr,font = ("Arial 15 bold"))

            self.scramblePic = tk.PhotoImage(file = self.resources + "cubelarge.gif")
            #os.remove("cubeimage.gif")
            self.scrambleImage = tk.Label(self.root,bg = "#BFBFBF" ,image = self.scramblePic)
            self.scrambleImage.place(relx = 0.97, rely = 0.97, anchor = tk.SE)
        else:
            self.get_scramble(False)       

            self.scramblePic = tk.PhotoImage(file = self.resources + "empty.gif" )   
            self.scrambleImage = tk.Label(self.root,bg = "#BFBFBF" ,image = self.scramblePic)
            self.scrambleImage.place(relx = 0.97, rely = 0.97, anchor = tk.SE)
 
        self.display.lift()

     
        #fill up listbox and get average
        if os.path.isfile(self.solvepath + "solves" + self.selectedCube.get() + ".txt"):
            solveFile = open(self.solvepath + "solves" + self.selectedCube.get() + ".txt")
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
 
        #GPIO pins 19 and 26
        self.button1 = Button(19)
        self.button2 = Button(26)
        
        self.delta = 0
        self.paused = True

        self.check_input()  
        self.root.mainloop()
        

    def connect_webserver(self,retry):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 8080))
            self.iplocal = (s.getsockname()[0])
            s.close()

            #start solves webserver (NOTE this is only a local webser on your own wifi. no one outside your setwork can access this
        
            if not self.system == "Windows":
                _thread.start_new_thread(os.system,('python3 ' + self.path + 'webserver/server.py' ,))
            else:
                _thread.start_new_thread(os.system,('python3 ' + self.path + 'webserver\\server.py' ,))
            
            #webserverip label 
            self.ipLabel = tk.Label(self.root,bg = "#BFBFBF", text= "Visit http://" + self.iplocal + ":8080\non your PC to export your solves", font = ("Arial 12")) 
            return
        except: 
            self.iplocal = "No internet connection"        
            if self.connectionAttempt:
                print(colored("Web server can't start since there is no internet connection","red")) 
            self.ipLabel = tk.Label(self.root,bg = "#BFBFBF", text= self.iplocal, font = ("Arial 12"))        
            
            if self.connectionAttempt:
                return
            self.connectionAttempt = True

        if retry:
            self.root.after(3000,self.connect_webserver(True))
        
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

    def inspection_timer(self): 
        while(True):
            self.delta = (time() - self.oldtime)
            #self.oldtime = time()
            secstr = int(self.delta)
            self.display.config(foreground = "red")    

            inspection = 15 - secstr

            self.display.config(text=inspection)
            if self.button1.is_pressed and self.button2.is_pressed:
                self.inspectionReady = True
                self.display.config(foreground = "green") 

            if not self.button1.is_pressed and not self.button2.is_pressed and self.inspectionReady:
                self.display.config(foreground = "black")
                return

            if(inspection < 0): 
                return

            self.display.update()

    def check_input(self):

        if self.button1.is_pressed and self.button2.is_pressed:

            if not self.paused:                

                self.display.config(foreground = "red")
   
                lastTime = self.display.cget("text")
                self.toggle()

                #this appends to a log file lawl
                solveStr = lastTime + " - " + self.lastScramble.replace("\n", "") 

                location = self.solvepath + "solves" + self.selectedCube.get() + ".txt"
                solveFile = open(location,"a")

                solveFile.write(solveStr + "\n") 
                _thread.start_new_thread(solveFile.close,())
        
                print(solveStr)
                
                self.solvesList.insert(0, ") " + lastTime) 
                self.solvesList.insert(1,self.lastScramble.replace("\n", ""))
                self.solvesList.insert(2," ")
                
                self.display.update_idletasks()

                self.set_average(5)                                  
                self.set_average(12)

                scramblestr = self.scramble.cget("text").replace("\n","")
                #self.scrambleImage.destroy()
            
                #open the image gif as binary data and read in the scramble that has been appended in the 
                #image generation program. if the scramble is the same as the current scramble then it will
                #show the image.
                if self.selectedCube.get() == "3x3x3":
                    try:
                        with open(self.resources + "cubelarge.gif", "rb") as last:
                            linelist = last.readlines()
                            last = linelist[len(linelist)-1].decode('ascii').replace("\n","")
                            print("image scramble: " + str(last) + "\ncurrent scramble: " + scramblestr) 

                        if last == scramblestr:
                            print("Scramble and image are equal")
                            self.scramblePic = tk.PhotoImage(file = self.resources + "cubelarge.gif")
                            self.scrambleImage = tk.Label(self.root,bg = "#BFBFBF" ,image = self.scramblePic)
                            self.scrambleImage.place(relx = 0.97, rely = 0.97, anchor = tk.SE)
                        else:
                            self.scramblePic = tk.PhotoImage(file = self.resources + "empty.gif")    
                    except:
                        self.scramblePic = tk.PhotoImage(file = self.resources + "empty.gif")
                        self.scrambleImage = tk.Label(self.root,bg = "#BFBFBF" ,image = self.scramblePic)
                        #if self.selectedCube.get() == "3x3x3":
                        #    self.scrambleImage.place(relx = 0.97, rely = 0.97, anchor = tk.SE)
                    
                        command = "python3 "+ self.path + "imagegen.py" + " \"" + scramblestr + "\""
                        _thread.start_new_thread(os.system,(command,))        
                        print("----------stop spamming so hard mitch----------")

                self.ao5Label.place(relx = 0.5, rely = 0.64, anchor = 'center')
                self.ao12Label.place(relx = 0.5, rely = 0.72, anchor = 'center') 
                self.infoButton.place(relx = 0.24, rely = 0.92, anchor = 'center') 
                self.settingsButton.place(relx = 0.09, rely = 0.92, anchor = 'center') 
                self.display.lift()
               
                if self.selectedCube.get() == "4x4x4" or self.selectedCube.get() == "5x5x5": 
                    self.scramble.place(relx = 0.5, rely = 0.16, anchor = 'center')
                if self.selectedCube.get() == "3x3x3" or self.selectedCube.get() == "2x2x2":
                    self.scramble.place(relx = 0.5, rely = 0.13, anchor = 'center')       
                if self.selectedCube.get() == "7x7x7" or self.selectedCube.get() == "6x6x6":
                    self.scramble.place(relx = 0.5, rely = 0.2, anchor = 'center')      
                
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
                
                self.lastScramble = self.scramble.cget("text")
                self.display.update_idletasks() 

                self.button1.wait_for_release()
                self.button2.wait_for_release()

                _thread.start_new_thread(self.get_scramble,(True,))

                if self.selectedInspection.get() == "Yes":
                    print("Inspecting...")
                    self.oldtime = time()
                    self.inspectionReady = False
                    self.inspection_timer()

                self.display.config(foreground = "black")
                self.toggle()

        

        if self.selectedCube.get() == "3x3x3" and not self.scrambleImage.winfo_ismapped() and self.scramble.winfo_ismapped():

            scramblestr = self.scramble.cget("text").replace("\n","")
            #self.scrambleImage.destroy()

            try: 
                with open(self.resources + "cubelarge.gif", "rb") as last:
                    linelist = last.readlines()
                    last = linelist[len(linelist)-1].decode('ascii').replace("\n","")
                    #print("second image scramble: " + str(last) + "\ncurrent scramble: " + scramblestr) 

                if last == scramblestr:
                    self.scramblePic = tk.PhotoImage(file = self.resources + "cubelarge.gif")
                    self.scrambleImage = tk.Label(self.root,bg = "#BFBFBF" ,image = self.scramblePic) 
                    if self.scramble.winfo_ismapped():
                        self.scrambleImage.place(relx = 0.97, rely = 0.97, anchor = tk.SE)
                else:
                    self.scramblePic = tk.PhotoImage(file = self.resources + "empty.gif")   
            except:
                self.scramblePic = tk.PhotoImage(file = self.resources + "empty.gif")
                self.scrambleImage = tk.Label(self.root,bg = "#BFBFBF" ,image = self.scramblePic)

        self.display.after(10,self.check_input)

    def view_solves(self):

        self.solvesList.pack(side = tk.LEFT,anchor = tk.NW,fill = tk.X)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.backButton.place(relx = 0.2, rely = 0.92, anchor = 'center')
        self.removeSelected.place(relx = 0.65, rely = 0.92, anchor = 'center') 
        
        self.solvesList.delete(0,tk.END)

        location = self.solvepath + "solves" + self.selectedCube.get() + ".txt"

        if os.path.isfile(location):
            solveFile = open(location)
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
                if len(current[1]) > 70:
                    lines = int(len(current[1]) / 40)
                    current[1] = self.split_scramble(current[1],lines)
                    splitScramble = current[1].split("\n")
                    
                    for i in range(len(splitScramble)):
                        self.solvesList.insert(tk.END,splitScramble[i])
 
                else:
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
        self.display.place(relx = 0.5, rely = 0.48, anchor = 'center')

        if self.selectedCube.get() == "4x4x4" or self.selectedCube.get() == "5x5x5": 
            self.scramble.place(relx = 0.5, rely = 0.16, anchor = 'center')
        if self.selectedCube.get() == "7x7x7" or self.selectedCube.get() == "6x6x6":
            self.scramble.place(relx = 0.5, rely = 0.2, anchor = 'center')
        if self.selectedCube.get() == "3x3x3" or self.selectedCube.get() == "2x2x2":
            self.scramble.place(relx = 0.5, rely = 0.13, anchor = 'center')
        self.infoButton.place(relx = 0.25, rely = 0.92, anchor = 'center') 
        self.ao5Label.place(relx = 0.5, rely = 0.64, anchor = 'center')
        self.ao12Label.place(relx = 0.5, rely = 0.72, anchor = 'center')
        self.settingsButton.place(relx = 0.08, rely = 0.92, anchor = 'center')
        
        if self.selectedCube.get() == "3x3x3":
            self.scrambleImage.place(relx = 0.97, rely = 0.97, anchor = tk.SE)
    
        self.display.lift()

        if self.logo.winfo_ismapped():
    
            with open(self.resources + "settings.txt", "w") as settingFile:
                settingFile.write(self.selectedCube.get() + "\n" + self.selectedInspection.get())

            if self.selectedCube.get() == "3x3x3" and not self.lastSelectedCube == "3x3x3":
                self.get_scramble(False)

                solvestr = self.scramble.cget("text").replace("\n","")

                command = 'python3 ' + self.path + 'imagegen.py' + ' \"' + solvestr  + '\"'
                os.system(command)
                self.scrambleImage.destroy()

                self.scramblePic = tk.PhotoImage(file = self.resources + "cubelarge.gif")
                self.scrambleImage = tk.Label(self.root,bg = "#BFBFBF" ,image = self.scramblePic)
                self.scrambleImage.place(relx = 0.97, rely = 0.97, anchor = tk.SE)
            elif not self.selectedCube.get() == "3x3x3":
                self.scrambleImage.place_forget()
                self.get_scramble(False)

            if self.ipLabel['text'] == "No internet connection":
                self.ipLabel.destroy()
                self.connect_webserver(False)
            
            self.solvesList.delete(0,tk.END)
            location = self.solvepath + "solves" + self.selectedCube.get() + ".txt"

            if os.path.isfile(location):
                solveFile = open(location)
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
                    if len(current[1]) > 70:
                        lines = int(len(current[1]) / 40)
                        current[1] = self.split_scramble(current[1],lines)
                        splitScramble = current[1].split("\n")
                    
                        for i in range(len(splitScramble)):
                            self.solvesList.insert(tk.END,splitScramble[i])
 
                    else:
                        self.solvesList.insert(tk.END,current[1])
                    self.solvesList.insert(tk.END," ") 

                solveFile.close() 

            self.set_average(5)
            self.set_average(12)
            self.display.update_idletasks()

  
        #print(self.selectedCube.get())

        self.backButton.place_forget()
        self.solvesList.pack_forget()
        self.scrollbar.pack_forget()
        self.removeSelected.place_forget()
        self.exit.place_forget()
        self.shutdown.place_forget()
        self.cubeDropdown.place_forget()
        self.logo.place_forget()
        self.dropdownLabel.place_forget()
        self.ipLabel.place_forget()
        self.inspectionDropdown.place_forget()
        self.inspectionLabel.place_forget()
        self.bar.place_forget()
        self.sleepButton.place_forget()

    def view_settings(self):
        self.lastSelectedCube = self.selectedCube.get()
 
        self.exit.place(relx = 0.28, rely = 0.92, anchor = 'center') 
        self.sleepButton.place(relx = 0.45, rely = 0.92, anchor = 'center')  
        self.shutdown.place(relx = 0.85, rely = 0.92, anchor = 'center')
        self.backButton.place(relx = 0.11, rely = 0.92, anchor = 'center')
        self.cubeDropdown.place(relx = 0.69, rely = 0.18, anchor = 'center')
        self.logo.place(relx = 0.28, rely = 0.5, anchor = 'center')
        self.dropdownLabel.place(relx = 0.76, rely = 0.045, anchor = 'center')
        self.ipLabel.place(relx = 0.28, rely = 0.08, anchor = 'center')
        self.inspectionDropdown.place(relx = 0.67, rely = 0.48, anchor = 'center')
        self.inspectionLabel.place(relx = 0.78, rely = 0.345, anchor = 'center')
        self.bar.place(relx = 0, rely = 0.82, anchor = tk.W)

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


        self.solvesList.delete(selection[0])            
        lineToDelete = selectedArray[0].strip()

        location = self.solvepath + "solves" + self.selectedCube.get() + ".txt"

        with open(location, "r") as solveFile:
            lines = solveFile.readlines()
        with open(location, "w") as solveFile:
            for line in lines:
                if not selectedArray[1] in line.strip("\n"):
                    solveFile.write(line)        

        print("Deleted solve #" + lineToDelete + ": " +selectedArray[1])
       
        self.set_average(5)
        self.set_average(12)
        self.view_solves()
        self.solvesList.see(selection[0])
            
    def set_average(self, number): 
        solveNum = 0

        for i in range(self.solvesList.size()):
            if "." in self.solvesList.get(i):
                solveNum += 1

        if solveNum >= number:

            aoArray = []
            for i in range(self.solvesList.size()):
                if "." in self.solvesList.get(i):
                    if ":" in self.solvesList.get(i).split(") ")[1]:
                        minute = self.solvesList.get(i).split(") ")[1].split(":")
                        secondsToAdd = float(float(minute[0]) * 60)
                        aoArray.append(float(float(minute[1]) + secondsToAdd))
                    else:
                        aoArray.append(float(self.solvesList.get(i).split(") ")[1])) 
                if len(aoArray) == number:
                    break
                                               
            top = aoArray[0]
            bot = aoArray[0]
            total = 0
 
            for j in range(number):
                if aoArray[j] > top:
                    top = aoArray[j]
                if aoArray[j] < bot:
                    bot = aoArray[j]
                    
            for j in range(number):
                if not aoArray[j] == top and not aoArray[j] == bot:
                    total += aoArray[j]
                    
            average = '%.2f' % (total / (number - 2))
            minstr = ((total / (number - 2))/60)

            if(int(minstr) > 0):
                secstr = '%.2f' % (float(average) - (int(minstr) * 60))
                if (float(average) - (int(minstr) * 60) )< 10: 
                    if number == 5:
                        self.ao5Label.config(text= "ao5: " + str(int(minstr)) + ":0" + str(secstr)) 
                    if number == 12:
                        self.ao12Label.config(text= "ao12: " + str(int(minstr)) + ":0" + str(secstr))
                else:
                    if number == 5:
                        self.ao5Label.config(text= "ao5: " + str(int(minstr)) + ":" + str(secstr)) 
                    if number == 12:
                        self.ao12Label.config(text= "ao12: " + str(int(minstr)) + ":" + str(secstr))
            else:
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
            stream = os.popen('head -n 1 ' + self.resources + 'scrambles333.txt')
            os.system('tail -n +2 "' + self.resources+ 'scrambles333.txt" > "' + self.resources + 'tmp.txt" && mv "' + self.resources + 'tmp.txt" "' + self.resources + 'scrambles333.txt"')       
            _thread.start_new_thread(self.scramble3, ())
            scramblestr = stream.read()

            if getImage:
                command = "python3 "+ self.path + "imagegen.py" + " \"" + scramblestr + "\""
                _thread.start_new_thread(os.system,(command,))        
 
            scramblestr = self.split_scramble(scramblestr,2) 
            self.scramble.config(text = scramblestr,font = ("Arial 15 bold"))

        if self.selectedCube.get() == "4x4x4":
            stream = os.popen('head -n 1 ' + self.resources + 'scrambles444.txt')
            os.system('tail -n +2 "' + self.resources+ 'scrambles444.txt" > "' + self.resources + 'tmp.txt" && mv "' + self.resources + 'tmp.txt" "' + self.resources + 'scrambles444.txt"')       
            _thread.start_new_thread(self.scramble4, ())
           
            scramblestr = stream.read()
            scramblestr = self.split_scramble(scramblestr,3)          
             
            self.scramble.config(text = scramblestr,font = ("Arial 14 bold"))

        if self.selectedCube.get() == "2x2x2":
            stream = os.popen('head -n 1 ' + self.resources + 'scrambles222.txt')
            os.system('tail -n +2 "' + self.resources+ 'scrambles222.txt" > "' + self.resources + 'tmp.txt" && mv "' + self.resources + 'tmp.txt" "' + self.resources + 'scrambles222.txt"')       
            _thread.start_new_thread(self.scramble2, ())
            scramblestr = stream.read()
            self.scramble.config(text = scramblestr,font = ("Arial 15 bold"))
        
        if self.selectedCube.get() == "5x5x5":
            stream = os.popen('head -n 1 ' + self.resources + 'scrambles555.txt')
            os.system('tail -n +2 "' + self.resources+ 'scrambles555.txt" > "' + self.resources + 'tmp.txt" && mv "' + self.resources + 'tmp.txt" "' + self.resources + 'scrambles555.txt"')       
            _thread.start_new_thread(self.scramble5, ())
 
            scramblestr = stream.read() 
            scramblestr = self.split_scramble(scramblestr,4)            

            self.scramble.config(text = scramblestr,font = ("Arial 12 bold"))
        
        if self.selectedCube.get() == "6x6x6":
            stream = os.popen('head -n 1 ' + self.resources + 'scrambles666.txt')
            os.system('tail -n +2 "' + self.resources+ 'scrambles666.txt" > "' + self.resources+ 'tmp.txt" && mv "' + self.resources + 'tmp.txt" "' + self.resources + 'scrambles666.txt"')       
            _thread.start_new_thread(self.scramble6, ())
            
            scramblestr = stream.read()           
            scramblestr = self.split_scramble(scramblestr,7)
 
            self.scramble.config(text = scramblestr,font = ("Arial 10 bold"))

        if self.selectedCube.get() == "7x7x7":
            stream = os.popen('head -n 1 ' + self.resources + 'scrambles777.txt')
            os.system('tail -n +2 "' + self.resources+ 'scrambles777.txt" > "' + self.resources+ 'tmp.txt" && mv "' + self.resources + 'tmp.txt" "' + self.resources + 'scrambles777.txt"')       
            _thread.start_new_thread(self.scramble7, ())
            
            scramblestr = stream.read()           
            scramblestr = self.split_scramble(scramblestr,7)
 
            self.scramble.config(text = scramblestr,font = ("Arial 10 bold"))

    def split_scramble(self,scramble,lines):

        split = int(len(scramble)/lines)

        for i in range(1,lines):
            if scramble[split*i] == " ":
                scramble = scramble[:split*i + 1] +  "\n" + scramble[split*i + 1:]
            elif scramble[split*i + 1] == " ":
                scramble = scramble[:split*i + 2] +  "\n" + scramble[split*i + 2:]
            elif scramble[split*i - 1] == " ":
                scramble = scramble[:split*i] +  "\n" + scramble[split*i:]
            elif scramble[split*i + 2] == " ":
                scramble = scramble[:split*i + 3] +  "\n" + scramble[split*i + 3:]
            else:
                scramble = scramble[:split*i - 1] +  "\n" + scramble[split*i - 1:]            
        
        return scramble

    def scramble3(self):

        with open(self.resources + "scrambles333.txt","a") as scrambleFile:
            print("Generating new 3x3 scramble")
            scrambleFile.write(scrambler333.get_WCA_scramble() + os.linesep)
            print("3x3 scramble generation complete")
    
    def scramble4(self):
        with open(self.resources+ "scrambles444.txt","a") as scrambleFile:
            print("Generating new 4x4 scramble")
            scrambleFile.write(scrambler444.get_WCA_scramble() + os.linesep)
            print("4x4 scramble generation complete")                                                                                
   
    def scramble2(self):
        with open(self.resources + "scrambles222.txt","a") as scrambleFile:
            print("Generating new 2x2 scramble")
            scrambleFile.write(scrambler222.get_WCA_scramble() + os.linesep)
            print("2x2 scramble generation complete")

    def scramble5(self):
        with open(self.resources + "scrambles555.txt","a") as scramblefile:
            print("Generating new 5x5 scramble")
            scramblefile.write(scrambler555.get_WCA_scramble() + os.linesep)
            print("5x5 scramble generation complete")
   
    def scramble6(self):
        with open(self.resources + "scrambles666.txt","a") as scramblefile:
            print("Generating new 6x6 scramble")
            scramblefile.write(scrambler666.get_WCA_scramble() + os.linesep)
            print("6x6 scramble generation complete")
    
    def scramble7(self):
        with open(self.resources + "scrambles777.txt","a") as scrambleFile:
            print("Generating new 7x7 scramble")
            scrambleFile.write(scrambler777.get_WCA_scramble() + os.linesep)
            print("7x7 scramble generation complete")

    def sleep_display(self):
        os.system("xset s 1")
        self.root.after(1000)
        os.system("xset s 0")

    def exit(self):   
        exit(0)

    def shutdown(self):
        call("sudo nohup shutdown -h now", shell=True)
 
Stopwatch()
