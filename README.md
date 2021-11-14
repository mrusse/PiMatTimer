# PiMat Timer
A full featured Rubik's cube timer made to run on a raspberry pi with a 3.5 inch touch screen. Inspiration taken from the stackmat timer for the
hardware and from csTimer for the software.

# Hardware
This timer is made to integrate with a 3d printed case I designed. The case integrates the 3.5 inch touch screen, a 10000mah battery and two buttons to start the timer stackmat style. The buttons connect to GPIO19 and GPIO26 (physical pins 35 and 37).
![3d printed case for the 3b+](https://i.imgur.com/IAsu6mP.jpg)
More information about the hardware will come soon.

# Installation
When cloning this repo to your pi make sure to also clone the submodules
```
git clone git@github.com:mrusse/PiMatTimer --recurse-submodules
```

Then install the requirments
```
python -m pip install -r requirements.txt
```
You could now run the program by doing ```python3 timer.py``` however you should setup the program to run at startup if you are using the pi as a dedicated timer.

You can use autostart to do this on the pi
```
mkdir /home/pi/.config/autostart
nano /home/pi/.config/autostart/timer.desktop
```
Then put this in the ```timer.desktop``` file.
```
[Desktop Entry]
Type=Application
Name=Timer
Exec=/usr/bin/python3 /home/pi/PiMatTimer/timer.py
```


![Main 3x3 screen](https://i.imgur.com/ArSZ5a5.png)

