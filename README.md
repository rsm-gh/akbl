
# Index
  * [Highlights](https://github.com/rsm-gh/akbl#highlights)
  * [Software Features](https://github.com/rsm-gh/akbl#about)
    * [Graphical Interface](https://github.com/rsm-gh/akbl#graphical-interface)
    * [System Tray Indicator](https://github.com/rsm-gh/akbl#system-tray-indicator)
    * [Default commands](https://github.com/rsm-gh/akbl#default-commands)
    * [Python Bindings](https://github.com/rsm-gh/akbl#python-bindings)
   
  * [How to Install](https://github.com/rsm-gh/akbl#how-to-install)
 
  * [F. A. Q.](https://github.com/rsm-gh/akbl#faq)
    * If my computer is not supported, what can I do?
    * How to use the block testing window?
    * After making changes to a theme, the changes are not applied
    * What's the function of the tempo button / clock icon / right-top corner button?

  * [Python Bindings](https://github.com/rsm-gh/akbl#python-bindings-1)
    * API
    * Testing all the commands
    * Changing the keyboard colors by checking the CPU Temperature
    * Changing the keyboard colors by checking the weather

  * [Documentation](https://github.com/rsm-gh/akbl#documentation)
  
  * [History](https://github.com/rsm-gh/akbl#history)
  
  * [About & Credits](https://github.com/rsm-gh/akbl#credits)
  

# Highlights

* 2022: **AKBL is not actively developed.** I almost stopped the development because I changed my latptop, so I have major limitations for using and testing the software.
* 2019: Many users with recent alienware computers are facing issues, probably because DELL has changed their USB protocol. Such computers are not supported, and you can find some interesting information in the open issues.

# Software Features

AKBL is a software to control the lights of Alienware computers (The keyboard, the logo, the speakers, etc...). It includes a Graphical Interphase, a System Try Indicator, Default Commands, and Python Bindings.

## Graphical Interface

![GUI](https://raw.githubusercontent.com/rsm-gh/akbl/stable/usr/share/doc/AKBL/ImagesPreview/GUI.png)

The GUI is designed to be easy and comfortable to use, it will allow you to easily create, delete, and modify profiles.

## System Tray Indicator

![System tray indicator](https://raw.githubusercontent.com/rsm-gh/akbl/stable/usr/share/doc/AKBL/ImagesPreview/Indicator.png)


It allows starting the GUI, turning the lights On/Off, and choosing profiles. By default, it is not enabled, but it can be added to the start session of a user with the command `akbl --start-indicator`.

## Default commands

```
Usage:

    akbl <option>

 Options:

    --change                          Change the computer lights on/off.
    --on                              Turn on the computer lights.
    --off                             Turn off the computer lights.
    --set-profile <profile_name>      Turn on the selected profile.
   
    --model-chooser                   Start the model chooser.   
   
    --start-indicator                 Start the indicator.
   
    --start-daemon                    Start the daemon.
    --daemon-is-on                    Return weather the daemon is running or not.
   
    --block-testing                   Display the block testing window.  
   
    -h, --help                        Display this dialog.
    -v, --version                     Display the software version. 
    -l, --license                     Display the software license.

 *If no option is introduced the graphical interface is launched.
```
The program comes with some default commands for those who don't know about programming. These commands can be easily added to hotkeys.

## Python Bindings

```python

import time, random
from AKBL.Bindings import Bindings

akbl = Bindings()
r = lambda: random.randint(0, 255)

while True:
    # Generate a random hex color
    random_hex_color = '#%02X%02X%02X' % (r(), r(), r())

    # Set the color in mode fixed
    akbl.set_colors('fixed', 100, random_hex_color)

    # Wait 2 seconds
    time.sleep(2)     
```
The Python bindings allow modifying the computer lights by using other program signals, for example, when receiving an email, when monitoring things like the weather or the CPU temperature. You can read more about this in the [Bindings section](https://github.com/rsm-gh/akbl#python-bindings-1).

# How to Install

1. Download the [stable branch](https://github.com/rsm-gh/akbl/archive/stable.zip).
2. Install the dependencies:

    * Debian based distributions: `apt-get install systemd libgtk-3-0 libgtk-3-dev gir1.2-ayatanaappindicator3-0.1 python3 python3-gi python3-cairo python3-usb python3-serpent python3-pyro4`.

    * ArchLinux: `pacman -Suy systemd gtk3 python python-gobject python-cairo python-pyusb python-serpent python-pyro` also `gir1.2-ayatanaappindicator3-0.1` is necessary for the app indicator, such dependency seems to be in the AUR.

3. Execute the setup file.

# F.A.Q.

### If my computer is not supported, what can I do?

Check if there's a bug concerning your computer model on GitHub, and if it doesn't exist, create one:

  1. Set the title of the bug as: "Add support to <computer model>"
  2. Fill the general information of the bug (GNU/Linux distribution, python version etc...)
  3. Add the USB data of your computer:  
   3.1 Open a terminal and execute the `lsusb` command:
```
  [rsm@m14xr1 ~]$ lsusb
  Bus 001 Device 004: ID 187c:0521 Alienware Corporation
  Bus 001 Device 003: ID 413c:8187 Dell Computer Corp. DW375 Bluetooth Module
  Bus 001 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
  Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
  Bus 003 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
  Bus 002 Device 002: ID 25a7:fa23 
  Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```
   
   3.2 Find the line with the Alienware device and get the bus and device numbers:
     
```
  Bus 001 Device 004: ID 187c:0521 Alienware Corporation
```

   3.3 Execute the `lsusb -D /dev/bus/usb/<bus>/<device>` command:
 
```
        [rsm@m14xr1 ~]$ lsusb -D /dev/bus/usb/001/004
        Device: ID 187c:0521 Alienware Corporation
        Couldn't open device, some information will be missing
        Device Descriptor:
          bLength                18
          bDescriptorType         1
          bcdUSB               1.10
          bDeviceClass            0
          bDeviceSubClass         0
          bDeviceProtocol         0
          bMaxPacketSize0        64
          idVendor           0x187c Alienware Corporation
        [etc...]
```

What will happen next?
  1. I'll take your Computer ID and Vendor ID, and I'll create a configuration file into `/usr/share/AKBL/computers/`.
  2. I'll commit the changes, and I'll request you to download it, install it, and test it.
  3. I'll wait to have your feedback (everything works, there are some problems, etc...). Please be specific! and give me as many details as possible!

If, after all, your computer is recognized, and you have minor problems (Ex: left and right keyboard), I'll commit the fixes.

If some zones are not recognized, I'll ask you to launch the block testing window to find the appropriate hex values. Once the blocks are found, I'll add them to the configuration file, and I'll commit the changes to the code.

### How to use the block testing window?

1. Execute as root `akbl --block-testing`.
2. A window will appear, and normally the ID Vendor and ID Product will be already filled. If not, akbl may not support your computer.
3. Click the Connect button, and the block testing block should be ready to be used.

The block testing will help you find the hex id's of your keyboard by iterating one by one the different possible hex values. Normally, the only thing you need to do is to change the Block Number combobox, and click the Test button.

When iterating over the block numbers, everything will be logged. Once that you have found a hex color of a zone, you can directly write the zone name. Here is an example:

```
## Text File ##

[Device found]: Vendor ID: 6268     Product ID: 1313


# This test turned on my left speaker
[Command]: Lights off
[TEST]: block: 32     hex: 0x20     mode:blink     speed:1     color1:#00ff00     color2: #00ff00


# This test turned on the akbl logo   
[Command]: Lights off
[TEST]: block: 256     hex: 0x100     mode:blink     speed:1     color1:#00ff00     color2: #00ff00
 ``` 

### After making changes to a theme, the changes are not applied

For the moment, the themes need to be saved before applying them. Any unsaved change will not be recognized by the daemon.

### What's the function of the tempo button / clock icon / right-top corner button?

That button manages the speed of the theme in the following cases:
  * When the section of a theme (keyboard-left, keyboard-right, etc..) has multiple zones.
  * When some zone has the morph (gradient) mode.
  * When some zone has the blink mode.

# Python Bindings

### API

```python
class Bindings:
       
    def reload_address(self):
        """
            It tries to make a connection with the Daemon, and it returns True or False.
        """
   
    def ping(self):
        """
            It checks if the Daemon is connected, and it returns True or False.
        """
   
    def get_address(self):
        """
            It returns the current URI of the Daemon.
        """
   
    def get_profile_names(self):
        """
            It returns a list of the existing profile names.
        """
       
    def set_profile(self, profile):
        """
            Set a profile from the existing profiles.
           
            + 'Profile' is the profile name.
        """
       
    def switch_lights(self):
           """
            Toggle on/off the lights of the keyboard.
           """
   
    def set_lights(self, state):
        """
            Turn the lights on or off.
           
            + 'state' can be a boolean or a string
        """
       
    def set_colors(self, mode, speed, colors1, colors2=None):
        """
            Change the colors and the mode of the keyboard.
           
            + The available modes are: 'fixed', 'morph' and 'blink',
                'fixed' and 'blink' only take 'colors1'.
               
            + Speed must be an integer. 1 =< speed =< 256
           
            + Colors1 and colors2 can be a single hex_color or a list
                of hex_colors. If both arguments are used, they must
                have the same number of items.
        """
```

### Testing all the commands

This is the example that I use to test the bindings. It should be clear enough to explain all the commands!

```python

# !/usr/bin/python3
#

import time
from AKBL.Bindings import Bindings

akbl = Bindings()

lights_test = True
profiles_test = True
colors_test = True
speed_test = True
colors_multiple_test = True

if not akbl.ping():
    print("The connection with the daemon is off")
    exit()

if lights_test:
    print('lights off', akbl.set_lights(False))
    time.sleep(2)
    print('lights on', akbl.set_lights(True))
    time.sleep(2)
    print('switch lights', akbl.switch_lights())

if profiles_test:
    for profile_name in akbl.get_profile_names():
        print('set profile:', profile_name, akbl.set_profile(profile_name))
        time.sleep(5)

color1 = '#F7F200'
color2 = '#0018FF'

if colors_test:
    print('set_colors blink', akbl.set_colors('blink', 100, color2))
    time.sleep(5)
    print('set_colors fixed', akbl.set_colors('fixed', 100, color1))
    time.sleep(5)
    print('set_colors morph', akbl.set_colors('morph', 100, color1, color2))

if speed_test:
    print('set_colors blink', akbl.set_colors('blink', 1, color2))
    time.sleep(5)
    print('set_colors blink', akbl.set_colors('blink', 100, color2))
    time.sleep(5)
    print('set_colors blink', akbl.set_colors('blink', 256, color2))
    time.sleep(5)

if colors_multiple_test:
    colors1 = '#0600FF'
    colors2 = '#FF00E5'

    print('set_colors multiple blink', akbl.set_colors('blink', 100, colors2))
    time.sleep(5)
    print('set_colors multiple morph', akbl.set_colors('morph', 100, colors1, colors2))
    time.sleep(5)
    print('set_colors multiple fixed', akbl.set_colors('fixed', 100, colors1))
```

### Changing the keyboard colors by checking the CPU Temperature

The following script will change the keyboard colors by checking the CPU Temperature. Before using the script, you should check in a terminal if you have the command `sensors`.

```python
#!/usr/bin/python3
#

import os
import time
from AKBL.Bindings import Bindings


def get_max_temp():
    """
        Get the maximum temperature of the CPU by
        using the bash commands "sensors"
    """
    output = os.popen('''sensors''')
    lines = output.readlines()

    max_temperature = 0

    for line in lines:
        if '°C' in line:
            temp = line.split('+')[1]
            temp = temp.split('°')[0]
            temp = float(temp)

            if temp > max_temperature:
                max_temperature = temp

    return max_temperature


def temperature_to_color(temp):
    """
        Map a temperature to a color. Return the color in HEX format.
    """
    if temp <= 0:
        hex_color = '#000000'  # black

    elif temp <= 20:
        hex_color = '#02EDFF'  # cyan

    elif temp <= 55:
        hex_color = '#0000FF'  # blue

    elif temp <= 70:
        hex_color = '#FFE900'  # yellow

    elif temp <= 85:
        hex_color = '#FF7800'  # orange

    else:
        hex_color = '#FF0014'  # red

    return hex_color


if __name__ == '__main__':

    akbl = Bindings()

    if not akbl.ping():
        print("The akbl daemon is off.")
        exit(1)

    while True:
        # Get the CPU temperature
        max_temp = get_max_temp()
        print("The maximum temperature is", max_temp)

        # Associate a color
        temp_color = temperature_to_color(max_temp)

        # Request AKBL to set the color
        akbl.set_colors('blink', 100, temp_color)

        # Wait and check again in X seconds
        time.sleep(5)
```

Note that if you want to test the code, you can create a fake temperature:

```python
max_temp=0
while True:
    
    # Get the CPU temperature
    #max_temp=get_max_temp()
    print("The maximum temperature is", max_temp)
    
    #
    # The rest of the code...
    #
    
    max_temp+=10
    time.sleep(5)
```

### Changing the keyboard colors by checking the weather

I was curious to find if there was command line weather program, and it seems that `inxi` works fine :)

```python

import os

def get_max_temp():
    """
        Get weather temperature and make a linear
        scale: 40°C <==> 100
       
        (The linear scale is only to adapt this function
         to the previous script)
    """
   
    # get the temperature
    output=os.popen('''inxi -w''')
    line=output.read()     
    try:
        temp_str=line.split(' C')[0].split('(')[1]
        max_temperature=float(temp_str)
    except Exception as e:
        print(e)
        max_temperature=0
       
    # adapt it
    max_temperature=(max_temperature*10)/4
 
    return max_temperature
```

so you can replace the function `get_max_temp` of the previous code, and it will now change the colors regarding the weather.

# Documentation
Some more diagrams and documentation can be found [here](https://github.com/rsm-gh/akbl/tree/stable/usr/share/doc/AKBL).

# History

AKBL stands for **A**lienware **K**ey**B**oard **L**ights (despite the fact that it controls much more than the keyboard). And I created my first version in 2014 by hacking PyAlienFX.  

It was a real hack from PyAlienFX because at that time I did not know about programming, and I only wanted to code a command for turning on and off the keyboard lights. So I mostly did some dirty modifications, and to avoid people blaming PyAlienFX for my code, I released it with a new name.

Then with the time, I realized that PyAlienFX was kinda dead, and I was having fun learning python with this software. So I started fixing bugs, removing proprietary content from the interface and creating new features. The major features that I have added are:

+ 2014: The Block Testing window. This is for debugging purposes.
+ 2015: The Daemon, which had as the main goal to allow the users to use the software without being root.
  + 2015: The System Try Indicator.
  + 2015: The Python Bindings. 

+ 2015-2016: Custom Debian Repository, Bug report pages, Sharing profiles pages, and chat hosted on my website (These features are not available anymore).  

+ XXXX: Improved the software architecture for maintenance purposes. And I also added some more friendly configuration files like the current INI files.

# About & Credits

This software is the work of libre software hackers of the GNU/Linux community. It does not depend on any corporation, and its code is licensed GPL3.

### AKBL

* Rafael Senties Martinelli

AKBL is a software based on PyAlienFX. I mostly created new addons, improved the software architecture, removed all the proprietary content, and fixed some bugs. Now days AKBL is like 98% different from pyAlienFX, but the code/concept that allows communicating with the hardware stills the same.

## PyALienFX

* Ledjfou125
* LightHash
* Corp
* Niai

As far as I know, pyAlienFX is not maintained anymore. They made work the project for some years, and at the start, they got inspired from AlienFX lite.


## AlienFX Lite

* Wattos

I have no information about AlienFX Lite, but in any case, Wattos was the first hacker to understand the USB communication and to make some code to work with. Definitely the most important work since DELL engineers have never helped us.


