**Index:**

* [Introduction](https://github.com/rsm-gh/alienware-kbl#introduction)
* [Installation instructions](https://github.com/rsm-gh/alienware-kbl#how-to-install)
* [Supported computers](https://github.com/rsm-gh/alienware-kbl#supported-computers)
* [F.A.Q.](https://github.com/rsm-gh/alienware-kbl#faq)
* [License](https://github.com/rsm-gh/alienware-kbl#license)
* [Credits](https://github.com/rsm-gh/alienware-kbl#credits)


## Introduction

Alienware-KBL is a software to control the lights of alienware computers under GNU/Linux systems. These are its main features:

* **A graphical interface**:  
![gui](https://cloud.githubusercontent.com/assets/11134652/24292992/f16cd1f6-108f-11e7-9257-650b34197d84.png)

* **A system-try indicator**:  
![indicator](https://cloud.githubusercontent.com/assets/11134652/24293017/0c107260-1090-11e7-8c57-ef52c8f9854a.png)

* [Python Bindings](https://github.com/rsm-gh/alienware-kbl/wiki/Python-Bindings)

* **Default commands**
```
Usage:

    alienware-kbl <option>

 Options:

    --change                          Changes the computer lights on/off.
    --on                              Turns on the computer lights.
    --off                             Turns off the computer lights.
    
    --set-profile <profile_name>      Turns on the selected profile.
    
    --start-indicator                 Start the indicator.
    
    --start-daemon                    Start the daemon.
    --daemon-is-on                    Returns weather the daemon is running or not.
    
    -h, -help                         Display this dialog.
    -l, --license                     Display the license.

 *If no option is introduced the graphical interface is launched.

```
	
## Installation instructions

1. Download the [stable branch](https://github.com/rsm-gh/alienware-kbl/archive/stable.zip)
2. Install the dependencies:
 * Debian Based Distributions: `apt-get install systemd gksu libgtk-3-0 libgtk-3-dev gir1.2-appindicator3-0.1 gir1.2-appindicator3 python3 python3-gi python3-cairo python3-usb python3-serpent python3-pip` and also use `pip3 install pyro`
 
    Note: `python3-pyro4` shall be `>= 4.47`, this is why it must be installed trought `python-pip`. 
 
 * ArchLinux: `pacman -S systemd gksu gtk3 libappindicator-gtk3 python python-cairo python-gobject python-pyusb python-pyro python-pip` and also use `pip install serpent`.
 
3. Execute the setup file

## Supported computers

***If your configuration is missing look at the [F.A.Q.](https://github.com/rsm-gh/alienware-kbl#faq) for the [support procedure](https://github.com/rsm-gh/alienware-kbl#my-computer-is-not-supported-what-can-i-do).**  
*The names & versions are taken from [this](https://en.wikipedia.org/wiki/Alienware) page of wikipedia.  

|Computer       |Status / Comment|
|---------------|----------------|
|Area 51-R1     |Eveything works good     |
|Area 51-R2     |Eveything works good     |
|Area 51-ALX-R1 |Configuration missing    |
|Aurora-R1      |Configuration missing    |
|Aurora-R2      |Configuration missing    |
|Aurora-R3      |Configuration missing    |
|Aurora-R4      |Configuration missing    |
|Aurora ALX-R1  |Configuration missing    |
|M11X-R1        |Eveything should work good      |
|M11X-R2        |Eveything works good            |
|M11X-R3        |Eveything works good            |
|M11X-R25       |Eveything works good            |
|M13X           |Configuration missing           |
|M14X-R1        |Eveything works good            |
|M14X-R2        |Eveything works good            |
|M14X-R3        |Eveything should work good      |
|M15X-R1        |Eveything should work good      |
|M15X-R2        |Eveything should work good      |
|Alienware 13   |Eveything works good            |
|Alienware 13-R2|Configuration missing           |
|Alienware 13-R3|It works, but with some problems|
|Alienware 15   |Eveything works good            |
|Alienware 15-R2|Configuration missing           |
|Alienware 15-R3|It works, but with some problems|
|M17X           |Eveything works good            |
|M17X-R1        |Configuration missing           |
|M17X-R2        |Configuration missing           |
|M17X-R3        |Eveything works good            |
|M17X-R4        |Configuration missing           |
|M17X-R5        |Configuration missing           |
|M18X-R1        |Configuration missing           |
|M18X-R2        |Eveything works good            |
|M18X-R3        |Configuration missing           |
|M18X-RX        |It works, but with some problems. It may be an R1 or R2|

## F.A.Q.

* [Is the software under development? How can I help?](https://github.com/rsm-gh/alienware-kbl#is-the-software-under-development-how-can-i-help)
* [Does it only works on GNU/Linux?](https://github.com/rsm-gh/alienware-kbl#does-it-only-works-on-gnulinux)
* [**My computer is not supported! What can I do?**](https://github.com/rsm-gh/alienware-kbl#my-computer-is-not-supported-what-can-i-do)
* [How to use the block testing window?](https://github.com/rsm-gh/alienware-kbl/https://github.com/rsm-gh/alienware-kbl#how-to-use-the-block-testing-window-)          
* [When I click the application icon nothing happens](https://github.com/rsm-gh/alienware-kbl#when-i-click-the-application-icon-nothing-happens)
* [After making changes to a theme the changes are not applied](https://github.com/rsm-gh/alienware-kbl#after-making-changes-to-a-theme-the-changes-are-not-applied)
* [The indicator, python bindings, commands and boot options don't work?](https://github.com/rsm-gh/alienware-kbl#the-indicator-python-bindings-commands-and-boot-options-dont-work)
* [What's the function of the tempo button / clock icon / right-top corner button?](https://github.com/rsm-gh/alienware-kbl#whats-the-function-of-the-tempo-button--clock-icon--right-top-corner-button)
* [When upgrading, the system try indicator indicates that the daemon is off](https://github.com/rsm-gh/alienware-kbl#when-upgrading-the-system-try-indicator-indicates-that-the-daemon-is-off)

## Is the software under development? How can I help?

I still maintaining the software but in reality it only changes when people submit bugs or request features. Except for one or two features that I would like to have, I consider that it is almost finished.

If you want to help the best you can do is submit bugs, <a href="https://github.com/rsm-gh/alienware-kbl/wiki">code</a> or help me to add support for new computers!

## Does it only works on GNU/Linux?

Yep, I only support [Libre Software](https://en.wikipedia.org/wiki/Free_software) and that includes developing only for free operating systems. 

Concerning my support, I currently use [ArchLinux](https://www.archlinux.org/) and while I'm not a fan of Ubuntu & derivatives, I try to give them support many people use them.

## My computer is not supported! What can I do?

The standard procedure to add a new computer to the configuration is the following:

1. Download & install alienware-kbl.
2. Launch the program, and open the window `Help > Computer Data`
3. Create a new bug report:
   1. Add the title `Add support to the <model> computer`
   2. Add the information of your operating system (Name and Version)
   3. Paste the text obtained from the window `Help > Computer Data`

What will happen next?

1. I'll take your `Computer ID` and `Vendor ID` and I'll add it to the `/usr/share/alienware-kbl/Computers.py` file, in to the `computerList` dictionary by choosing the closest configuration for your computer.
2. I'll commit the changes to the [testing branch](https://github.com/rsm-gh/alienware-kbl/tree/testing), and I'll request you to [download it](https://github.com/rsm-gh/alienware-kbl/archive/testing.zip), install it, and test it.
3. I'll wait to have your feed back, "everything works", "there are some problems", etc.. please be specific, and give me as much details as possible!

If your computer is then recognized but you have minor problems (Ex: left and right keyboard), Thanks to your feedback, I'll make the fixes and I'll commit them. 

Otherwise, if you have complex problems and some zones are recognized at all, I'll ask you to launch `alienware-kbl` as root, and to use the [`Help > Block Testing`](https://github.com/rsm-gh/alienware-kbl#the-block-testing-window-works-but-with-the-default-settings-do-not-change-them) window to find the appropriate hex values. Once that you have find them, I'll commit the changes and the computer will be supported ;}

Notes:
* If you have any problem performing the steps, post it under the bug that you have open !
* If you understand the code you can directly make a push the modifications :)


## How to use the block testing window ?

**The block testing window does not exist anymore. Since October 29 2017 it went removed from the sable branch**

1. Launch `alienware-kbl` as root.
2. Open the window `Help > Block Testing`
3. Normally the `ID Vendor` and `ID Product` fields will be automatically filled. If not, the software may not support your computer.
4. Click, the `Connect` button, and you will be able to start making tests.

The block testing will help you to find the hex values of your computer zones by iterating the values one by one. Normally, the only thing you need to do is to change the `Block Number` combobox and to click the `TEST BLOCK` button. If the block concern some zone of the computer, after hitting the `TEST BLOCK` button it should turn on.

Everything you do will be logged including possible program errors, and if everything goes well and you find some computer zone, you can directly add some `# comments`.


Here is an example of the log:
```
[Device found]: Vendor ID: 6268	 Product ID: 1313


# This test turned on my left speaker
[Command]: Lights off
[TEST]: block: 32	 hex: 0x20	 mode:blink	 speed:1	 color1:#00ff00	 color2: #00ff00


# This test turned on the alienware-kbl logo    
[Command]: Lights off
[TEST]: block: 256	 hex: 0x100	 mode:blink	 speed:1	 color1:#00ff00	 color2: #00ff00 
```    
            
## When I click the application icon nothing happens

It seems that some distributions have problems to launch the program with `gksu`. The simpler way of checking this to launch `alienware-kbl` as root. In any cases, if you have this problem I'll appreciate that you make a bug report!

## After making changes to a theme the changes are not applied

The software offers the possibility of using the graphical interface without root permission. When doing this, the themes need to be saved before applying them, if not the changes will not be visible.

## The indicator, python bindings, commands and boot options don't work?

The problem is that those three features use the daemon, so it means that the daemon is off. This is normal on distributions that do not use [systemd](https://en.wikipedia.org/wiki/Systemd).

It is possible to manually start the daemon as root `setsid alienware-kbl --start-daemon` but take care of having only one running instance.

## What's the function of the tempo button / clock icon / right-top corner button?

That button manages the speed of the theme in the following cases:

* When the section of a theme (keyboard-left, keyboard-right, etc..) has multiple zones
* When some zone has the morph (gradient) mode
* When some zone has the blink mode

Normally the program does not allow to set the speed value equal to 0, so if your theme contain any of the previous cases, you should being able of noticing the speed effects. In case you don't see it, I'd suggest to increment the speed before opening a bug report.

## When upgrading, the system try indicator indicates that the daemon is off

That is normal because when making the installation the daemon is restarted. If you want to reset the indicator without rebooting or closing your current session, just exit the current indicator and launch a new instance from the terminal by using `alienware-kbl --start-indicator`. 

It is not advisable to have multiple indicators running at the same time!

## License

The code is licensed [GPL3](./usr/share/doc/alienware-kbl/GPL3) and the artwork [CC-BY-4.0](./usr/share/doc/alienware-kbl/CC-BY-4.0). 

## Credits

The software has been developed with the contributions of many GNU/Linux users and hackers, it does not belong to any corporation and it shouldn't be confused with a formal projet !

**Alienware-KBL**

* Rafael Senties Martinelli
* Amalia Angeli (ArtWork)

**PyALienFX**

* Ledjfou125
* LightHash
* Corp
* Niai

**AlienFX Lite**

* Wattos

Beside the main code of the software, some users have contributed to make the software support the configuration of their computer, these are some of the names:

* Alienware 13 by Francesco Rosa
* M11XR1 by aehs29
* M11XR2 by iferlive
* M14XR1 by LightHash
* M14XR3 by nshp
* Alienware 15 by trollsid
* M17XR3 by Niai
* M18XR2 by SuperTool
