
# How to develop alienware-kbl?

1. Install the dependencies:
  * Debian based distributions: `apt-get install systemd gksu libgtk-3-0 libgtk-3-dev gir1.2-appindicator3-0.1 gir1.2-appindicator3 python3 python3-gi python3-cairo python3-usb python3-serpent python3-pip` and also use `pip3 install pyro`
  Note: `python3-pyro4` shall be `>= 4.47`, this is why it must be installed trought `python-pip`.
  
  * ArchLinux: `pacman -S systemd gksu gtk3 libappindicator-gtk3 python python-cairo python-gobject python-pyusb python-pyro python-pip` and also use `pip install serpent`.

2. Download the branch.

3. Open two terminals, one as root and one as normal user.

4. Under the root terminal:
    1. Change the working directory to the one of the project: `cd alienware-kbl`.
    
    2. Everytime that you want to test your implementations use the following command: `./setup && systemd stop alienware-kbl && alienware-kbl --start-daemon`.
    
    If you made implementations to the Daemon you will be then able to see them if you execute them under `__init__`, and if that's not the case, well, use the addon that you want to test and you will see the debug messsages either in the Daemon terminal or in the addon terminal.

  **Bonnus:** reasons and explanation of the previous commands:
  
  `./setup` is used to install the software. This is necessary for the develop part because:
   + The daemon must be launched as root.
   + Some paths point to `/usr/share/`.
   + The daemon must be launched from the ` alienware-kbl ` bash script since it is necessary to use the USB patch.
   + `systemd stop alienware-kbl && alienware-kbl --start-daemon` is used to load the daemon on the current terminal. `systemd stop alienware-kbl` stops the daemon started by the installation  and `alienware-kbl --start-daemon` starts the daemon in the current terminal. 
  
  Note that it is not advisable to run two daemon instances because the pyro communication system will probably fail or choose only one daemon to speak.

# Development documentation

## General architecture

![General Diagram](https://github.com/rsm-gh/alienware-kbl/blob/new-version/usr/share/doc/AlienwareKBL/Programming/general%20diagram.png)


I'm currently debugin the Daemon and the Bindings.


# What are the main changes if we compare this version to the stable branch?

+ The code was simplified and organized, even some good PEP8 rules went added.
+ The debug/warning/error system was improved.
+ The GUI doesn't use anymore the root account.

This changes are so important because `alienware-kbl` is as a community project and everyone should be able of understanding it so it can be enhanced.
Also having a clear and non-redundant code enhances the performances and makes it a much better software!

# What is missing to implement?

1) Find out why `alienware-kbl -off` & `alienware-kbl --on` are not working.
2) (Optional) Finish the block testing window:
  This window was made as a friendly inferface so developers be able to play & test the alienware bus system with `python-usb`.
  Because `python-usb` will require root permission, this window shall be taken off the GUI and even be developed as a separate software from `alienware-kbl`.

  Concerning this window, I made it work and it was functional. You can read more about it at the F.A.Q.

# Optional known bugs/features that would be nice to fix:
+ Directly load the daemon from a root session without using the libusb patch.
+ Concerning the GUI:
  + Fix the power button.
  + Add the different blocks (On save, On boot, On battery). For this you can take a look in to the pyAlienFX project.
