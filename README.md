**Alienware-KBL is not anymore under development. You can either use the [functional stable branch](https://github.com/rsm-gh/alienware-kbl/tree/stable) or continue this branch and create a new project.**

# About

For me this branch is the future of `alienware-kbl`. A really cool branch with lots of new code ideas and implementations.
It makes me feel sad to suddendly stop the project, but I stopped coding outside of my job.

You're free to download, modify and share the code, I added as much as information as possible so anyone be able of moving the project to the new step :)

My only petition is that your project be renamed so people can find figure out that it is a new project. I actually refuse to use the Mozilla license so if you want to thank me, respecting my philosofphy is the best way ;)


# How to use and develop this branch?

1. Install the dependencies:
  * Debian based distributions: `apt-get install systemd gksu libgtk-3-0 libgtk-3-dev gir1.2-appindicator3-0.1 gir1.2-appindicator3 python3 python3-gi python3-cairo python3-usb python3-serpent python3-pip` and also use `pip3 install pyro`
  Note: `python3-pyro4` shall be `>= 4.47`, this is why it must be installed trought `python-pip`.
  
  * ArchLinux: `pacman -S systemd gksu gtk3 libappindicator-gtk3 python python-cairo python-gobject python-pyusb python-pyro python-pip` and also use `pip install serpent`.

2. Download the branch.

3. Open two terminals, one as root and one as normal user.

4. Under the root terminal:
    1. Change the working directory to the one of the project: `cd alienware-kbl`.
    
    2. Everytime that you want to test your implementations use the following command: `./setup && systemd stop alienware-kbl && alienware-kbl --start-daemon`.
    
    3. Under the normal user terminal execute some daemon command. Ex: `alienware-kbl --off`, `alienware-kbl --on`.
  
  You will be then able of testing and debuging the daemon since this is the first step to make the whole program work.

  **Bonnus** reason and explanation of the previous commands:
  
  `./setup` is used to install the software. This is necessary for the develop part because:
   + The daemon must be launched as root.
   + Some paths point to `/usr/share/`.
   + The daemon must be launched from the ` alienware-kbl ` bash script since it is necessary to add an USB patch export (I never found how to do this from python).
  
  `systemd stop alienware-kbl && alienware-kbl --start-daemon` is used to load the daemon on the current terminal:
  
   + `systemd stop alienware-kbl` stops the daemon after the installation (because by default the installation loads the daemon and enables it at boot).
  
  + `alienware-kbl --start-daemon` launches the daemon at the current terminal. Note that it is not advisable to run two daemon instances because the pyro communication system will probably fail or choose only one daemon to speak.


# The new software diagram

![General Diagram](https://github.com/rsm-gh/alienware-kbl/blob/new-version/usr/share/doc/AlienwareKBL/Programming/general%20diagram.png)


This branch is the future of alienware-kbl, the goals are to:

+ The `block testing window` will be separated from the GUI.
+ The GUI will no longer use the root account.
    * The Daemon will be mandatory for using the GUI
    * gksu will be removed as dependence


# What are the main changes if we compare this version to the stable branch?

+ The code was simplified and organized, even some good PEP8 rules went added.
+ The debug/warning/error system was improved.
+ The GUI doesn't use anymore the root account.

This changes are so important because `alienware-kbl` is as a community project and everyone should be able of understanding it so it can be enhanced.
Also having a clear and non-redundant code enhances the performances and makes it a much better software!

# What is missing to implement?

1) Find out why `alienware-kbl -off` & `alienware-kbl --on` is not working.
2) (Optional) Finish the block testing window:
  This window was made as a friendly inferface so developers be able to play & test the alienware bus system with `python-usb`.
  Because `python-usb` will require root permission, this window shall be taken off the GUI and even be developed as a separate software from `alienware-kbl`.

  Concerning this window, I made it work and it was functional. You can read more about it at the F.A.Q.

# Optional known bugs/features that would be nice to fix:
+ Directly load the daemon from a root session without using the libusb patch.
+ Concerning the GUI:
  + Fix the power button.
  + Add the different blocks (On save, On boot, On battery). For this you can take a look in to the pyAlienFX project.
  
# What else?

That's all the information. I wish you a happy hacking ;}


