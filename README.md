**Index:**

* [Introduction](https://github.com/rsm-gh/alienware-kbl#introduction)
* [Installation instructions](https://github.com/rsm-gh/alienware-kbl#how-to-install)
* [Supported computers](https://github.com/rsm-gh/alienware-kbl#supported-computers)
* [F.A.Q.](https://github.com/rsm-gh/alienware-kbl/wiki/F.A.Q.)
* [License](https://github.com/rsm-gh/alienware-kbl#license)
* [Credits](https://github.com/rsm-gh/alienware-kbl#credits)


## Introduction

Alienware-KBL is a software to control the lights of alienware computers under GNU/Linux systems. These are its main features:

* **A graphical interface**:  
![gui](https://cloud.githubusercontent.com/assets/11134652/24292992/f16cd1f6-108f-11e7-9257-650b34197d84.png)

* **A system-try indicator**:  
![indicator](https://cloud.githubusercontent.com/assets/11134652/24293017/0c107260-1090-11e7-8c57-ef52c8f9854a.png)

* [Python Bindings](https://github.com/rsm-gh/alienware-kbl/wiki/Python-Bindings)
* [Default commands](https://github.com/rsm-gh/alienware-kbl/wiki/Default-Commands)
	
## Installation instructions

1. Download the stable branch
2. Install the dependencies:
 * Debian Based Distributions: `apt-get install systemd gksu libgtk-3-0 libgtk-3-dev gir1.2-appindicator3-0.1 gir1.2-appindicator3 python3 python3-gi python3-cairo python3-usb python3-serpent python3-pip` and also use `pip3 install pyro`
 
    Note: `python3-pyro4` shall be `>= 4.47`, this is why it must be installed trought `python-pip`. 
 
 * ArchLinux: `pacman -S systemd gksu gtk3 libappindicator-gtk3 python python-cairo python-gobject python-pyusb python-pyro python-pip` and also use `pip install serpent`.
 
3. Execute the setup file

## Supported computers

*If your computer is not supported look at the [F.A.Q.](https://github.com/rsm-gh/alienware-kbl/wiki/F.A.Q.#) for the [support procedure](https://github.com/rsm-gh/alienware-kbl/wiki/F.A.Q.#my-computer-is-not-supported-what-can-i-do).  
*The names & versions are taken from [this](https://en.wikipedia.org/wiki/Alienware) page of wikipedia.  

|Symbol | Meaning                                  |
|-------|------------------------------------------|
|:)     | Eveything works good (confirmed)         |
|:?     | Eveything works good (not confirmed)     |
|:S     | It works, but with some problems         |
|:/     | Configuration missing / untested computer|

|Computer       |Status  |Comment|
|---------------|--------|-------|
|Area 51-R1     |:?      ||
|Area 51-R2     |:?      ||
|Area 51-ALX-R1 |:/      ||
|Aurora-R1      |:/      ||
|Aurora-R2      |:/      ||
|Aurora-R3      |:/      ||
|Aurora-R4      |:/      ||
|Aurora ALX-R1  |:/      ||
|M11X-R1        |:?      ||
|M11X-R2        |:?      ||
|M11X-R3        |:?      ||
|M11X-R25       |:?      ||
|M13X           |:/      ||
|M14X-R1        |:)      ||
|M14X-R2        |:)      ||
|M14X-R3        |:?      ||
|M15X-R1        |:?      ||
|M15X-R2        |:?      ||
|Alienware 13   |:)      ||
|Alienware 13-R2|:/      ||
|Alienware 13-R3|:S      ||
|Alienware 15   |:)      ||
|Alienware 15-R2|:/      ||
|Alienware 15-R3|:S      ||
|M17X           |:)      ||
|M17X-R1        |:/      ||
|M17X-R2        |:/      ||
|M17X-R3        |:)      ||
|M17X-R4        |:/      ||
|M17X-R5        |:/      ||
|M18X-R1        |:/      ||
|M18X-R2        |:)      ||
|M18X-R3        |:/      ||
|M18X-RX        |:S      |It may be an R1 or R2|

## [F.A.Q.](https://github.com/rsm-gh/alienware-kbl/wiki/F.A.Q.)

Please look at the [F.A.Q.](https://github.com/rsm-gh/alienware-kbl/wiki/F.A.Q.) before asking questions and submiting bugs !

## License

The code is licensed [GPL3](./usr/share/doc/alienware-kbl/GPL3) and the artwork [CC-BY-4.0](./usr/share/doc/alienware-kbl/CC-BY-4.0), for more details look at the [copyright file](./usr/share/doc/alienware-kbl/copyright). 

## Credits

The software has been developed with the contributions many GNU/Linux users and hackers. It doesn't belongs any corporation and it should not be confused with a formal projet.

Alienware-KBL is based on [pyAlienFX](https://github.com/Xqua/pyAlienFX), which was based on AlienFX Lite. These are the main credits and contributors:

	
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

Beside the main code of the software, some users have contributed to the support configuration of their computer, this are some of the names:

* Alienware 13 by Francesco Rosa
* M11XR1 by aehs29
* M11XR2 by iferlive
* M14XR1 by LightHash
* M14XR3 by nshp
* Alienware 15 by trollsid
* M17XR3 by Niai
* M18XR2 by SuperTool





