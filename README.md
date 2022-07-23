
**Before requesting support please consider that AKBL is not actively developed.** I changed my computer in 2022, so I can't use or test the software anymore.

Also since 2019 many users with recent alienware computers are facing issues, probably because DELL has changed the USB protocol and it is different from the old computers. Such computers are not yet supported and some interesting information and code can be found in the open issues.

Best regards,  
rsm~

----
----

# Index
  
  * [Software Features](https://github.com/rsm-gh/akbl#about)
    * [Graphical Interface](https://github.com/rsm-gh/akbl#graphical-interface)
    * [System Tray Indicator](https://github.com/rsm-gh/akbl#system-tray-indicator)
    * [Default commands](https://github.com/rsm-gh/akbl#default-commands)
    * [Python Bindings](https://github.com/rsm-gh/akbl#python-bindings)
   
  * [How to Install](https://github.com/rsm-gh/akbl#how-to-install)
 
  * [F. A. Q.](https://github.com/rsm-gh/akbl#faq)
    * If my computer is not supported, what can I do?
    * How to use the block testing window?
    * After making changes to a theme the changes are not applied
    * What's the function of the tempo button / clock icon / right-top corner button?
    * Why there are no distribution packages and the installation is so complex? 

  * [Python Bindings](https://github.com/rsm-gh/akbl#python-bindings-1)
    * API
    * Testing all the commands
    * Changing the keyboard colors by checking the CPU Temperature
    * Changing the keyboard colors by checking the weather

  * [Development Documentation](https://github.com/rsm-gh/akbl#development-documentation)
    * Global Communication
  
  * [AKBL History](https://github.com/rsm-gh/akbl#akbl-history)
    * History
    * Extra 
  
  * [About & Credits](https://github.com/rsm-gh/akbl#credits)
  



# Software Features

AKBL is a software to control the lights of Alienware computers (The keyboard, the logo, the speakers, etc..). It includes a Graphical Interphase, a System Try Indicator, Default Commands, and Python Bindings.

## Graphical Interface

![GUI](https://raw.githubusercontent.com/rsm-gh/akbl/stable/usr/share/doc/AKBL/ImagesPreview/GUI.png)

The GUI is designed to be easy and comfortable to use, it will allow you to easily create, delete, and modify profiles.

## System Tray Indicator

![System tray indicator](https://raw.githubusercontent.com/rsm-gh/akbl/stable/usr/share/doc/AKBL/ImagesPreview/Indicator.png)


It allows starting the GUI, turning the lights On/Off, and choosing profiles. By default it is not enabled, but it can be added to the start session of a user with the command `akbl --start-indicator`.

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
The program comes with some default commands for those who doesn't know about programming. These commands can be easily added to hotkeys.

## Python Bindings

```python

import time, random
from AlienwareKBL import AlienwareKBL
   
akbl=AlienwareKBL()
r = lambda: random.randint(0,255)
 
while True:
 
    # Generate a random hex color
    random_hex_color='#%02X%02X%02X' % (r(),r(),r())   
 
    # Set the color in mode fixed
    akbl.set_colors('fixed', 100, random_hex_color)
 
    # Wait 2 seconds
    time.sleep(2)     
```
The Python bindings allow to modify the computer lights by using other programs signals, for example  when receiving an email, when monitoring things like the weather or the CPU temperature. You can read more about this in the [Bindings section](https://github.com/rsm-gh/akbl#python-bindings-1).

# How to Install

1. Download the [stable branch](https://github.com/rsm-gh/akbl/archive/stable.zip).
2. Install the dependencies:

    * Debian based distributions: `apt-get install systemd libgtk-3-0 libgtk-3-dev gir1.2-ayatanaappindicator3-0.1 python3 python3-gi python3-cairo python3-usb python3-serpent python3-pyro4`.

    * ArchLinux: `pacman -Suy systemd gtk3 python python-gobject python-cairo python-pyusb python-serpent python-pyro` also `gir1.2-ayatanaappindicator3-0.1` is necessary for the app indicator, such dependency seems to be in the AUR.

3. Execute the setup file.

*Note: If you wonder why there are no installation packages, you can refer to [this question](https://github.com/rsm-gh/akbl/blob/stable/README.md#why-there-are-no-distribution-packages-and-the-installation-is-so-complex).*

# F.A.Q.

### If my computer is not supported, what can I do?

Check if there's a bug concerning your computer model on GitHub, and if it don't exists create one:

  1. Set the title of the bug as: "Add support to (computer model)"
  2. Fill the general information of the bug (GNU/Linux distribution, python version etc)..
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
  1. I'll take your Computer ID and Vendor ID and I'll create a configuration file into `/usr/share/AKBL/computers/`.
  2. I'll commit the changes and I'll request you to download it, install it and test it.
  3. I'll wait to have your feed back (everything works, there are some problems, etc..). Please be specific! and give me as much details as possible!

If after all that your computer is recognized and you have minor problems (Ex: left and right keyboard), I'll commit the fixes.

If some zones are not recognized, I'll ask you to launch the block testing window to find the appropriate hex values. Once the blocks found, I'll add them to the configuration file, and I'll commit the changes to the code.

### How to use the block testing window?

1. Execute as root `akbl --block-testing`.
2. A window will appear and normally the ID Vendor and ID Product will be already filled. If not, akbl may not support your computer.
3. Click, the Connect button, and the block testing block should be ready to be used.

The block testing will help you to find the hex id's of your keyboard by iterating one by one the different possible hex values. Normally, the only thing you need to do, is to change the Block Number combobox, and click the Test button.

When iterating over the block numbers, everything will be logged. Once that you have found an hex color of a zone, you can directly write the zone name. Here is an example:

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

### After making changes to a theme the changes are not applied

For the moment the themes need to be saved before applying them. Any unsaved change will not be recognized by the daemon.

### What's the function of the tempo button / clock icon / right-top corner button?

That button manages the speed of the theme in the following cases:
  * When the section of a theme (keyboard-left, keyboard-right, etc..) has multiple zones.
  * When some zone has the morph (gradient) mode.
  * When some zone has the blink mode.

### Why there are no distribution packages and the installation is so complex? 

Here is one good part of the answer:

* Why not use `setuptools`:

  * It does not feed some needs like installing systemd files.
  * This module should always be avoided because all the software of a distribution shall be managed by the package manager.
  * This feature may be interesting for python software that is multi-operative system, which is not the case for AKBL.

* Why not to let distributions do their thing?

  * Normally the GNU/Linux software is always released with installation batchs, and then, the maintainers of each Distribution create a custom package and include it into their repositories. If you a maintainer you can feel free to do that.
  * In the old times (before 2016) I used to create Debian packages and I even had my own repository, but I do not have the time to maintain it anymore. It is too much time consuming to release packages for each distribution (Debian, Noobuntu, ArchLinux..).
  * Create a package means that I made a release, I don't release AKBL.

* Why not create a binary?

  * Even if you can compile python code, I don't think that you will be able to include all the dependencies which some may be written in other languages.
  * There is no much sense in compiling python software that is free code.

* Why not using custom paths?

  * The software files are kinda "complex". There are:
    * Python module files
    * Common resource files
    * Binary files
    * User files
    * Systemd files
    * Temp files
    * Communication files

    and every single file has a special location defined by GNU/Linux conventions. This should not be customized by an user. If you really want to do this, you can modify the setup script, and the paths python file.

* Why using a batch:
  * Because it is the common way to install GNU/Linux software that do not comes from any repository.
  * Because it allows to do anything that it is necessary to do (Move files, start services, etc etc..).
  * Because it works for any GNU/Linux distribution. I do not need to pass hours checking the dependencies of each distribution and making tests.
  * Because it does not requires to release the code, it can be directly taken from GIT, which allows much more flexibility.


# Python Bindings

### API

```python
class AlienwareKBL():
       
    def reload_address(self):
        """
            It tries to make a connection with the Daemon
        and it returns True or False.
        """
   
    def ping(self):
        """
            It checks if the Daemon is connected
            and it returns True or False.
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
           
            + 'profile' is the profile name.
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
           
            + colors1 and colors2 can be a single hex_color or a list
          of hex_colors. If both arguments are used, they must
          have the same number of items.
        """
 
```

### Testing all the commands

This is the example that I use to test the bindings. It should be clear enough to explain all the commands !

```python

#!/usr/bin/python3
#
 
import time
from AKBL.Bindings import Bindings
 
AKBLConnection=Bindings()
 
lights_test=True
profiles_test=True
colors_test=True
speed_test=True
colors_multiple_test=True
 
 
if not AKBLConnection.ping():
    print("The connection with the daemon is off")
    exit()
 
 
 """
     Each command is called as:
    
         print( <command_name>, <command> )
        
     To check if the commands succeed. You don't
     really need to do this in your code!
 """
 
 if lights_test:
     print('lights off', AKBLConnection.set_lights(False))
     time.sleep(2)
     print('lights on', AKBLConnection.set_lights(True))
     time.sleep(2)
     print('switch lights', AKBLConnection.switch_lights())
 
 
 if profiles_test:
     for profile_name in AKBLConnection.get_profile_names():
         print('set profile:', profile_name, AKBLConnection.set_profile(profile_name))
         time.sleep(5)
 
 
 color1='#F7F200'
 color2='#0018FF'
 
 if colors_test:
     print('set_colors blink', AKBLConnection.set_colors('blink', 100, color2))
     time.sleep(5)
     print('set_colors fixed', AKBLConnection.set_colors('fixed', 100, color1))
     time.sleep(5)
     print('set_colors morph', AKBLConnection.set_colors('morph', 100, color1, color2))
 
     
 if speed_test:
     print('set_colors blink', AKBLConnection.set_colors('blink', 1, color2))
     time.sleep(5)
     print('set_colors blink', AKBLConnection.set_colors('blink', 100, color2))
     time.sleep(5)
     print('set_colors blink', AKBLConnection.set_colors('blink', 256, color2))
     time.sleep(5)
 
 
 if colors_multiple_test:
     colors1='#0600FF'
     colors2='#FF00E5'
     
     print('set_colors multiple blink', AKBLConnection.set_colors('blink', 100, colors2))
     time.sleep(5)
     print('set_colors multiple morph', AKBLConnection.set_colors('morph', 100, colors1, colors2))
     time.sleep(5)
     print('set_colors multiple fixed', AKBLConnection.set_colors('fixed', 100, colors1))
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
    output=os.popen('''sensors''')
    lines= output.readlines()
   
    max_temperature=0
   
    for line in lines:
        if '°C' in line:
            temp = line.split('+')[1]
            temp = temp.split('°')[0]
            temp = float(temp)
           
            if temp > max_temperature:
                max_temperature=temp
           
    return max_temperature     
 
 
if __name__ == '__main__':
 
    akbl=Bindings()
 
    if not akbl.ping():
        print("The akbl daemon is off.")
    else:
        while True:
           
            max_temperature=get_max_temp()
            print("The maximum temperature is", max_temperature)
           
            if max_temperature <= 0:
                akbl.set_colors('fixed', 100, '#000000') # black
            elif max_temperature <= 20:
                akbl.set_colors('fixed', 100, '#02EDFF') # cyan
            elif max_temperature <= 55:
                akbl.set_colors('fixed', 100, '#0000FF') # blue
            elif max_temperature <= 70:
                akbl.set_colors('fixed', 100, '#FFE900') # yellow
            elif max_temperature <= 85:
                akbl.set_colors('fixed', 100, '#FF7800') # orange
            elif max_temperature <= 95:
                akbl.set_colors('fixed', 100, '#FF0014') # red
            else:
                akbl.set_colors('blink', 100, '#FF0014') # red
 
            time.sleep(5) # seconds

```

Note that if you want to test the code, you can just create a fake temperature:

```python

else:
    max_temperature=0
    while True:
        #max_temperature=get_max_temp()
                .
                .
                .
        max_temperature+=10
        time.sleep(5)
```

### Changing the keyboard colors by checking the weather

I was curious to find if there was command line weather program, and it seems that `inxi` works fine :)


```python

#!/usr/bin/python3
#
 
import os
import time
from AKBL.Bindings import Bindings
 
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
 
 
if __name__ == '__main__':
 
    akbl=Bindings()
 
    if not akbl.ping():
        print("The akbl daemon is off.")
    else:
        while True:
           
            max_temperature=get_max_temp()
            print("The maximum temperature is", max_temperature)
           
            if max_temperature <= 0:
                akbl.set_colors('fixed', 100, '#000000') # black
            elif max_temperature <= 20:
                akbl.set_colors('fixed', 100, '#02EDFF') # cyan
            elif max_temperature <= 55:
                akbl.set_colors('fixed', 100, '#0000FF') # blue
            elif max_temperature <= 70:
                akbl.set_colors('fixed', 100, '#FFE900') # yellow
            elif max_temperature <= 85:
                akbl.set_colors('fixed', 100, '#FF7800') # orange
            elif max_temperature <= 95:
                akbl.set_colors('fixed', 100, '#FF0014') # red
            else:
                akbl.set_colors('blink', 100, '#FF0014') # red
 
            time.sleep(5) # seconds   
           
```

# Development Documentation

## Global Communication
![general diagram](https://raw.githubusercontent.com/rsm-gh/akbl/stable/usr/share/doc/AKBL/Programming/general%20diagram.png)

[...] Some more diagrams and documentation can be found [here](https://github.com/rsm-gh/akbl/tree/stable/usr/share/doc/AKBL)

# AKBL History

## History
AKBL stands for **A**lienware **K**ey**B**oard **L**ights (despite the fact that it controlls much more than the keyboard). And I created my first version in 2014 by hacking PyAlienFX.  

It was a real hack from PyAlienFX because at that time I did not know about programming, and I only wanted to code a command for turning on and off the keyboard lights. So I mostly did some dirty modifications, and to avoid people blaming PyAlienFX for my code, I released it with a new name.

Then with the time, I realized that PyAlienFX was kinda dead and I was having fun learning python with this software. So I started fixing bugs, removing private content from the interface and creating new features. The major features that I have added are:

+ 2014: The Block Testing window. This is for debugging purposes.
+ 2015: The Daemon which had as main goal to allow the users using the software without being root.
  + 2015: The System Try Indicator.
  + 2015: The Python Bindings. 

+ XXXX: Improved the software architecture for maintenance purposes. And I also added some more friendly configuration files like the current INI files.

So mostly I've been coding AKBL since 2014, doing modifications from time to time, and saddly despite the fact that alot of users contact me for bugs and new features, no one else have ever contributed directly to the code. The problem about this, is that I'm the only developer, and my free time for the project is very limited.

I may continue developing AKBL until my M14XR1 dies, but then I don't think I´ll buy another Alienware Laptop, I'll get some tiny and low performance computer.


## Extra
With the time I have removed some content. In 2015-2016 AKBL was purely hosted on my personal website and I had some features like the Debian Repository, the Bug report pages, the sharing profiles pages, and the custom website.  

Then, I realized that all those features was taking a lot of work and I spent more time doing extra stuff than actually coding AKBL, so I decided to remove most of the features and add the project to GitHub.

Some years after, I got back online with my personal website and I re-included the AKBL web page and a custom chat, but again, in 2020 I started developing other projects and I decided to close my personal website.

Even if the features was really nice, I do not have the time to maintain them. I'd better spend the few time that I have in the software it self.




# About & Credits

This software is the work of libre software hackers of the GNU/Linux community. It do not depends of any corporation and its code is licensed GPL3.

### AKBL

* Rafael Senties Martinelli

AKBL is a software based on PyAlienFX. I mostly created new addons, improved the software architecture, removed all the privative content, and fixed some bugs. Now days AKBL is like 98% different from pyAlienFX but the code/concept that allows communicating with the hardware stills the same.

## PyALienFX

* Ledjfou125
* LightHash
* Corp
* Niai

As far as I know pyAlienFX is not maintained anymore. They made work the project for some years and at the start they got inspired from AlienFX lite.


## AlienFX Lite

* Wattos

I have no information about AlienFX Lite, but in any case Wattos was the first hacker to understand the USB communication and to make some code to work with. Definitely the most important work since DELL engineers have never help us.


