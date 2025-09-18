#!/bin/bash

#
# This file is part of AKBL.
#
#  Copyright (C) 2015-2025 Rafael Senties Martinelli.
#
# This work is free. You can redistribute it and/or modify it under the
# terms of the CC0 1.0 Universal (CC0 1.0) Public Domain Dedication.
# <https://creativecommons.org/publicdomain/zero/1.0/>
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


if [ "$EUID" -ne 0 ]
  then echo -e "\e[00;31m The script must be run as root.\e[00m"
  exit
fi

NUMBER_OF_STEPS=6 			# installation steps

#
# Set the scripts permissions
#
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
chmod a+x "$DIR/uninstall.bash"

#
# Remove previous versions
#
echo -e "\e[00;33m[1/$NUMBER_OF_STEPS] Removing previous versions..\e[00m"
"$DIR/uninstall.bash"

#
# Start the installation
#
echo -e "\e[00;33m\n[2/$NUMBER_OF_STEPS] Installing the software files...\e[00m"

function install_files(){
    
    echo "installing: $1"

    if [ -d "$DIR$1/__pycache__" ]; then
      rm -rf "$DIR$1/__pycache__"
    fi

    install -d "$1" |& grep -v "omitting directory"
    install -D "$DIR$1/"* "$1" |& grep -v "omitting directory"
    
}

install_files "/usr/bin"

install_files "/usr/share/applications"
install_files "/usr/share/AKBL"
install_files "/usr/share/AKBL/test"
install_files "/usr/share/AKBL/computers"
install_files "/usr/share/AKBL/GUI"
install_files "/usr/share/AKBL/GUI/ColorChooserToolbar"
install_files "/usr/share/AKBL/GUI/img"
install_files "/usr/share/AKBL/BlockTesting"
install_files "/usr/share/AKBL/Indicator"
install_files "/usr/share/AKBL/Indicator/img"
install_files "/usr/share/AKBL/ModelChooser"

install_files "/usr/share/doc/AKBL"
install_files "/usr/share/doc/AKBL/BusData"
install_files "/usr/share/doc/AKBL/BusData/Data"
install_files "/usr/share/doc/AKBL/ImagesPreview"
install_files "/usr/share/doc/AKBL/Licenses"
install_files "/usr/share/doc/AKBL/Programming"
install_files "/usr/share/doc/AKBL/Programming/class_diagrams"

install_files "/usr/lib/python3/AKBL"
install_files "/usr/lib/python3/AKBL/Engine"
install_files "/usr/lib/python3/AKBL/Computer"
install_files "/usr/lib/python3/AKBL/Theme"

install_files "/usr/lib/systemd/system"
chmod u=rw /usr/lib/systemd/system/akbl.service # The permissions must be forced.
chmod go=r /usr/lib/systemd/system/akbl.service # The permissions must be forced.

##
## Post installation
##

echo -e "\e[00;33m\n[3/$NUMBER_OF_STEPS] Creating the python links...\e[00m"

for python_directory in /usr/lib/python3*; do

  if [[ "$python_directory" != "/usr/lib/python3" ]]; then

    if [ -d "$python_directory" ]; then
        ln -s /usr/lib/python3/AKBL "$python_directory/AKBL" && echo -e "Linked $python_directory"
    fi
  fi

done

echo -e "\e[00;33m\n[4/$NUMBER_OF_STEPS] Choosing the computer model...\e[00m"
python3 /usr/share/AKBL/ModelChooser/cmd.py


echo -e "\e[00;33m\n[5/$NUMBER_OF_STEPS] Enabling the daemon...\e[00m"
if [ -f /bin/systemctl ]; then
    systemctl daemon-reload
    systemctl enable akbl
    systemctl restart akbl
    sleep 2
else
	echo -e "\e[00;31m Warning: systemd seems to be missing. The daemon will have to be manually launched.\e[00m"
fi

echo -e "\e[00;33m\n[6/$NUMBER_OF_STEPS] Testing the installation...\e[00m"
echo -e "AKBL version: $(akbl --version)"

ping=$(akbl --ping)

if [[ "$ping" == "False" ]]; then
  echo -e "\e[00;31mThe daemon ping is OFF, to make the software work you need to correct this problem.\e[00m"
elif [[ "$ping" == "True" ]]; then
  echo -e "\033[0;32The installation has finished. If you have any window of the software (GUI, BlockTesting, Bindings script, etc..) or the indicator is running, you must restart them.\e[00m\n"
else
  echo -e "\e[00;31mThe installation was not successful.\e[00m"
fi
