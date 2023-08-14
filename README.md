# PiMat Timer
A full-featured Rubik's cube timer made to run on a Raspberry Pi running Raspberry Pi OS. Inspiration taken from the stackmat timer for the
hardware and from csTimer for the software.


### Example solves and feature presentation video 
[![Example Solves and Feature Presentation](https://i.imgur.com/VXLWDD7.png)](https://www.youtube.com/watch?v=ox_MspGBqCA)

# Hardware
This timer is made to integrate with a 3d printed case I designed. The case integrates a 3.5 inch touch screen, a 10000mah battery, and two buttons to start and stop the timer stackmat style. The buttons connect to GPIO19 and GPIO26 (physical pins 35 and 37).

![3d printed case for the 3b+](https://i.imgur.com/IAsu6mP.jpg)

[View the design on Printables to learn more](https://www.printables.com/model/240596-pimat-rubiks-cube-timer)

# Installation
Make sure your username on the Raspberry Pi is `pi` and that you clone this repo in the `$HOME` directory (e.g., `/home/pi`). The script assumes these paths. Run `cd ~` if you are unsure if you're in the home directory.

When cloning this repo to your pi make sure to also clone the submodules ([access denied (publickey) error?](#access-denied)):
```
cd ~
git clone git@github.com:mrusse/PiMatTimer --recurse-submodules
```

Then install the requirments
```
python -m pip install -r requirements.txt
```

The program also requires nodejs so install that on the pi if you don't have it already
```
sudo apt-get install nodejs
```

You could now run the program by doing ```python3 timer.py``` however you should setup the program to run at startup if you are using the pi as a dedicated timer. If the timer does not start, check out the troubleshooting below.

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
Save and exit with ```ctrl + x```, followed by ```y``` when prompted to save, and then ```enter```. Reboot with:
```
sudo reboot
```
The program should now launch on start up

# Features

The timer can provide scrambles for 2x2 - 7x7 and also has a scramble image tool for 3x3. The main screen will also display your current average of 5 and 12 similar to csTimer

Every scramble the timer uses is generated using the pyTwistyScrambler module which can generate WCA random state scrambles.
However to reduce lag there is a buffer file of scrambles that is used. Each time you complete a solve it pulls a new scramble from the 
buffer file, deletes that scramble from the file, then in a new thread adds a new scramble generated by pyTwistyScrambler to the end of the file.
It is done this way since there is a delay in generating these random state scrambles on the pi (about 3 seconds). So using this file
buffer method the experience is seamless.

### Main timer screen with 3x3 scramble and image.

![Main 3x3 screen](https://i.imgur.com/6rO6vGL.png)

### Solves list screen which lists all your solves in the current session

You can select a time and click ```Delete Selected Time``` to remove that solve. Each session (2x2 - 7x7) will store their times seperatly.

![3x3 solves screen](https://i.imgur.com/FS5S4Jt.png)

### Settings menu

In the settings you can change your puzzle type and turn on or off WCA inspection. You also have access to some system controls here such as the option to shutdown the pi or exit the program.

If the pi has a wifi connection it will also show the link to a local webserver where you can export your solves or download a current screenshot of the program. (View image below)

![Settings menu](https://i.imgur.com/ZZB3fiO.png)

### Local webserver

![Webserver](https://i.imgur.com/E1XCaKx.png)

### Example of a 5x5 session and solves

![5x5 session](https://i.imgur.com/xjU86jv.png)

![5x5 solves](https://i.imgur.com/nuAKNQR.png)

## Troubleshooting

### Access Denied

If you don't have a GitHub account or SSH credentials set up, you will get an access denied (publickey) error because of GitHub's security concerns.

Aside from creating a GitHub account and setting that up, you can also make Git clone from HTTPS instead of SSH:

```bash
# Use HTTPS instead of SSH by default
git config --global url."https://github.com/".insteadOf git@github.com:

# Clone the repo and its submodules
git clone git@github.com:mrusse/PiMatTimer --recurse-submodules

# Undo the HTTPS setting
git config --global --unset url."https://github.com/".insteadOf
```

Even though it is possible to `git clone https://github.com/mrusse/PiMatTimer`, Git will still default to SSH, which will still throw the error during the cloning of the submodules.

### `_tkinter.TclError: no display name and no $DISPLAY environment variable`
Got this issue on a Raspberry Pi 4 Model B Rev1.1; solution was to `export DISPLAY=:0.0`, but to make this setting persist on reboot you'll need to add it to your `.*rc` file (e.g., append it to the bottom of `~/.bashrc` or `~/.zshrc`, whichever file exists).