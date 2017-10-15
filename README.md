
# How to develop alienware-kbl?

1. Install the dependencies:
  * Debian based distributions: `apt-get install systemd gksu libgtk-3-0 libgtk-3-dev gir1.2-appindicator3-0.1 gir1.2-appindicator3 python3 python3-gi python3-cairo python3-usb python3-serpent python3-pip` and also use `pip3 install pyro`
  Note: `python3-pyro4` shall be `>= 4.47`, this is why it must be installed trought `python-pip`.
  
  * ArchLinux: `pacman -S systemd gksu gtk3 libappindicator-gtk3 python python-cairo python-gobject python-pyusb python-pyro python-pip` and also use `pip install serpent`.

2. Download the branch.

3. Open two terminals, one as root and one as normal user.

4. Under the root terminal:
    1. Change the working directory to the one of the project: `cd alienware-kbl`.
    
Then everytime that you want to test your implementations use the following command: `reset && ./setup && systemd stop alienware-kbl && alienware-kbl --start-daemon`.

If you made implementations to the Daemon you will be then able to see them if you execute them under `__init__`, and if that's not the case, well, use the addon that you want to test and you will see the debug messsages either in the Daemon terminal or in the addon terminal.

  **Bonnus:** reasons and explanation of the previous commands:
  
  `reset` is used to clear the terminal.
  
  `./setup` is used to install the software. This is necessary for the develop part because:
   + The daemon must be launched as root.
   + Some paths point to `/usr/share/`.
   + The daemon must be launched from the ` alienware-kbl ` bash script since it is necessary to use the USB patch.
  
  `systemd stop alienware-kbl && alienware-kbl --start-daemon` is used to load the daemon in the current terminal. `systemd stop alienware-kbl` stops the daemon started by the installation  and `alienware-kbl --start-daemon` starts the daemon in the current terminal. 
  
  *It is not advisable to run multiple daemon instances because the pyro communication system will probably fail or choose only one daemon to speak.*

# Development documentation

## General architecture

![General Diagram](https://github.com/rsm-gh/alienware-kbl/blob/new-version/usr/share/doc/AlienwareKBL/Programming/general%20diagram.png)
