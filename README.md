
Alienware-KBl is a software to control the lights of alienware computers and it commes with the following features:

* A graphical interface
* [Python Bindings](https://github.com/rsm-gh/alienware-kbl/wiki/Python-Bindings)
* [Default commands](https://github.com/rsm-gh/alienware-kbl/wiki/Default-Commands)
* A system-try Indicator

	
## How to Install

1. Download the stable branch
2. Install the dependencies:
 * Debian Based Distributions: `apt-get install systemd gksu libgtk-3-0 libgtk-3-dev gir1.2-appindicator3-0.1 gir1.2-appindicator3 python3 python3-gi python3-cairo python3-usb python3-serpent python3-pyro4`
 
 * ArchLinux: `pacman -S systemd gksu gtk3 libappindicator-gtk3 python python-cairo python-gobject python-pyusb python-pyro python-pip` and also use `pip install serpent`.
 
3. Execute the setup file

## Supported Computers
```
Legend:
  :) = Eveything works good (confirmed)
  :? = Eveything works good (not confirmed)
  :S = It works, but with some problems
  :/ = Configuration missing
```
If your computer is not supported, look at the [F.A.Q.](https://github.com/rsm-gh/alienware-kbl/wiki/F.A.Q.#) for the [support procedure](https://github.com/rsm-gh/alienware-kbl/wiki/F.A.Q.#my-computer-is-not-supported).

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
|Alienware 15   |:)      ||
|Alienware 15-R3|:S      |Added in to the testing branch. [#8](https://github.com/rsm-gh/alienware-kbl/issues/8)|
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

*The names & versions are taken from [this](https://en.wikipedia.org/wiki/Alienware) page of wikipedia.

## [F.A.Q.](https://github.com/rsm-gh/alienware-kbl/wiki/F.A.Q.)

## License

The code is licensed GPL3 and the artwork CC-BY. For more details look at the copyright file placed under `./usr/share/doc/alienware-kbl/`

## [Credits](https://github.com/rsm-gh/alienware-kbl/wiki/Credits)
