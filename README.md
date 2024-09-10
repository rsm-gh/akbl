
# Index
  * [Highlights](https://github.com/rsm-gh/akbl#highlights)
  * [Software Features](https://github.com/rsm-gh/akbl#about)
  * [How to Install](https://github.com/rsm-gh/akbl#how-to-install)
  * [F. A. Q.](https://github.com/rsm-gh/akbl#faq)
  * [Python Bindings](https://github.com/rsm-gh/akbl#python-bindings-1)
  * [Documentation](https://github.com/rsm-gh/akbl#documentation)
  * [History](https://github.com/rsm-gh/akbl#history)
  * [About & Credits](https://github.com/rsm-gh/akbl#credits)
  

# Highlights

* 2022: The software cannot be correctly tested since I changed my laptop. I do not possess an Alienware computer any more.
* 2019: Many users with recent Alienware computers are facing issues, probably because DELL has changed their USB protocol. Such computers are not supported, and you can find some interesting information in the open issues.

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

    --on                              Turn on the computer lights.
    --off                             Turn off the computer lights.
    --switch                          Switch the computer lights on/off.
    --set-theme <theme_name>          Set the selected theme (on).
    
    --model-chooser-gui               Launch the model chooser from a GUI.
    --model-chooser-cmd               Launch the model chooser from a CMD.
    
    --start-indicator                 Start the indicator.
    --start-white-indicator           Start the indicator (with white icons).
    
    --start-daemon                    Start the daemon.
    --ping                            Check if the Daemon is connected and ready to execute commands.
    
    --block-testing                   Launch the block testing window.
    
    -h, --help                        Display this dialog.
    -v, --version                     Display the software version.  
    -l, --license                     Display the software license.

 *If no option is introduced the graphical interface is launched.
```
The program comes with some default commands for those who don't know about programming.
These commands can be easily added to hotkeys.
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
    akbl.set_fixed_mode([random_hex_color], 100)

    # Wait 2 seconds
    time.sleep(2)     
```
The Python bindings allow modifying the computer lights by using other program signals, for example, when receiving an email, when monitoring things like the weather or the CPU temperature. You can read more about this in the [Bindings section](https://github.com/rsm-gh/akbl#python-bindings-1).

# How to Install

1. Download the [stable branch](https://github.com/rsm-gh/akbl/archive/stable.zip).
2. Install the dependencies:

    * Debian-based distributions:
      + Core: `systemd usbutils python3 python3-usb python3-pyro4`.
      + GUI: `libgtk-3-0 libgtk-3-dev python3-gi python3-cairo` and `gir1.2-ayatanaappindicator3-0.1` for the app indicator.

    * ArchLinux:
       + Core: `systemd usbutils python python-pyusb python-pyro`.
       + GUI:  `webkit2gtk python-gobject python-cairo`) `gir1.2-ayatanaappindicator3-0.1` from the AUR for the app indicator.

3. Execute the setup file.

# F.A.Q.

### If my computer is not supported, what can I do?

Check if there's a bug concerning your computer model on GitHub, and if it doesn't exist, create one:

  1. Set the title of the bug as: "Add support to <computer model>"
  2. Fill the general information of the bug (GNU/Linux distribution, python version, etc...)
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

If some areas are not recognized, I'll ask you to launch the block testing window to find the appropriate hex values. Once the blocks are found, I'll add them to the configuration file, and I'll commit the changes to the code.

### Block Testing Window: How to use it?

1. Execute as root `akbl --block-testing`.
2. A window will appear, and normally the ID Vendor and ID Product will be already filled. If not, akbl may not support your computer.
3. Click the Connect button, and the block testing block should be ready to be used.

The block testing will help you find the hex id's of your keyboard by iterating one by one the different possible hex values. Normally, the only thing you need to do is to change the Block Number combobox and click the Test button.

When iterating over the block numbers, everything will be logged. Once that you have found a hex color of an area, you can directly write the areaitem name. Here is an example:

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

### GUI: After making changes to a theme, the changes are not applied

This is because the themes need to be saved before applying them. Any unsaved change will not be recognized by the daemon.

### GUI: What's the function of the tempo button / clock icon / right-top corner button?

That button manages the speed of the theme in the following cases:
  * When the section of a theme (keyboard-left, keyboard-right, etc...) has multiple areas.
  * When some areaitem has the morph (gradient) mode.
  * When some areaitem has the blink mode.

### GUI: What's the difference between "Apply theme" & "Lights on"?

* Apply them will apply the current theme that it's selected in the GUI.
* Lights on will apply either:
  * The last modified theme, if the lights have not been turned on (by the same user).
  * The last theme used for turning the lights on.

Note: these to buttons have the same behavior as the CMD commands `akbl --on` and `akbl --set-theme <name>`.

# Python Bindings

### API

```python
class Bindings:
       
    def ping(self) -> bool:
        """Check if the Daemon is connected and ready to execute commands."""

    def reload_address(self, verbose=False) -> bool:
        """Reload the pyro address and try to make a connection with the Daemon."""
        
    def switch_lights(self) -> None:
        """Switch the lights on or off."""

    def get_themes_name(self) -> list[str]:
        """Return a list of the existing user themes."""
       
    def get_computer_name(self) -> str:
        """Get the computer name set by AKBL."""
        
    def set_theme(self, theme_name: str) -> bool:
        """Set a theme by name."""
   
    def set_lights(self, state: bool) -> None:
        """Set the lights on or off."""
       
    def set_fixed_mode(self,
                       colors: list[str],
                       speed: int = 1) -> bool:
        """
            Change all the light areas with the fixed mode. Each color of the list will
            be set in all the areas, and it will move to the next value depending on the speed.

            If only one color is provided, the lights will remain at one single color and the speed
            will not have any effect.

            :param list[str] colors: A list of Hex colors.
            :param int speed: Speed for switching each areaitem to the next color, 1 =< speed >= 256.
        """

    def set_blink_mode(self,
                       colors: list[str],
                       speed: int = 50) -> bool:
        """
            Change all the light areas, with the blink mode. Each color of the list will
            be set in all the areas, and it will blink depending on the speed.

            :param list[str] colors: A list of Hex colors.
            :param int speed: Speed for blinking, 1 =< speed >= 256.
        """

    def set_morph_mode(self,
                       colors: list[tuple[str, str], ...],
                       speed: int = 50) -> bool:
        """
            Change all the light areas, with the morph mode. Each color pair of the list will
            be set in all the areas, and it will create a gradient from the first color, to
            the second color, depending on the speed.

            :param list[tuple(str, str)] colors: A list of lists containing two values of Hex colors.
            :param int speed: Speed for switching each areaitem to the next color, 1 =< speed >= 256.
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
modes_test = True
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
    for theme_name in akbl.get_themes_name():
        print('set theme:', theme_name, akbl.set_theme(theme_name))
        time.sleep(5)

single_colors = ['#F7F200']
morph_colors = [('#F7F200', '#ff0000')]

if modes_test:
    print("\nModes test")
    print('\tset_colors fixed', akbl.set_fixed_mode(single_colors, 100))
    time.sleep(5)
    print('\tset_colors blink', akbl.set_blink_mode(single_colors, 100))
    time.sleep(5)
    print('\tset_colors morph', akbl.set_morph_mode(morph_colors, 100))
    time.sleep(5)

if speed_test:
    print("\nSpeed test on mode blink")
    print('\tset_colors: speed=1', akbl.set_blink_mode(single_colors, 1))
    time.sleep(5)
    print('\tset_colors: speed=100', akbl.set_blink_mode(single_colors, 100))
    time.sleep(5)
    print('\tset_colors: speed=255', akbl.set_blink_mode(single_colors, 255))
    time.sleep(5)

if colors_multiple_test:
    print("\nMultiple colors test")
    single_colors = ['#FF0000', '#FFFF00', '#3F33FF']  # red, yellow, #blue
    morph_colors = [('#FF0000', '#3F33FF'),
                    ('#FFFF00', '#3F33FF'),
                    ('#FF0000', '#3F33FF')]

    print('\tset_colors: multiple fixed', akbl.set_fixed_mode(single_colors, 100))
    time.sleep(15)
    print('\tset_colors: multiple blink', akbl.set_blink_mode(single_colors, 100))
    time.sleep(15)
    print('\tset_colors: multiple morph', akbl.set_morph_mode(morph_colors, 100))
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
        akbl.set_blink_mode([temp_color], 100)

        # Wait and check again in X seconds
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

+ Improved the software architecture for maintenance purposes. And I also added some more friendly configuration files like the current INI files.

# About & Credits

This software is the work of libre-software hackers of the GNU/Linux community. It does not depend on any corporation, and its code is licensed GPL3.

### AKBL

* Rafael Senties Martinelli

AKBL is a software based on PyAlienFX. I mostly created new addons, improved the software architecture, removed all the proprietary content, and fixed some bugs. Nowadays AKBL is like 98% different from pyAlienFX, but the code/concept that allows communicating with the hardware stills is the same.

## PyALienFX

* Founded125
* LightHash
* Corp
* Niai

As far as I know, pyAlienFX is not maintained anymore. They made work the project for some years, and at the start, they got inspired by AlienFX lite.


## AlienFX Lite

* Wattos

I have no information about AlienFX Lite, but in any case, Wattos was the first hacker to understand the USB communication and to make some code to work with. Definitely the most important work since DELL engineers have never helped us.


