#!/bin/bash

#
# Public domain.
#
#
# uninstall.bash by Rafael Senties Martinelli.
#
# To the extent possible under law, the person who associated CC0 with
# uninstall.bash has waived all copyright and related or neighboring rights
# to uninstall.bash.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.


if [ "$EUID" -ne 0 ]
  then echo "The script must be run as root."
  exit
fi

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "$DIR" || exit

if [ -f /bin/systemctl ]; then
	echo -e "\e[00;33mDisabling the systemd daemon...\033[0m"
    systemctl stop akbl
    systemctl disable akbl
    echo ""
fi

echo -e "\e[00;33mRemoving the python links..\033[0m"

for python_directory in /usr/lib/python3*; do

    echo -e "Checking $python_directory"

    if [[ -L "$python_directory/AKBL" ]]; then
      rm -f "$python_directory/AKBL" && echo -e "- Link removed"
    fi

    if [ -f "$python_directory/AKBL" ] || [ -f "$python_directory/AKBL.py" ]; then
        rm -f "$python_directory/AKBL" && echo -e "- File removed"
    fi

    if [ -d "$python_directory/AKBL" ] || [ -d "$python_directory/AKBL.py" ]; then
        rm -rf "$python_directory/AKBL.py" && echo -e "- Directory removed"
    fi

done

echo ""



echo -e "\e[00;33mRemoving the software files and directories..\033[0m"


function remove_file(){
     
    if [ -f "$1" ]; then
        rm -f "$1"
        echo "removed.f: $1"
    fi
}

function remove_dir(){
     
    if [ -d "$1" ]; then
        rm -rf "$1"
        echo "removed.d: $1"
    fi
}

remove_file "/usr/share/applications/AKBL.desktop"
remove_file "/usr/share/applications/com.senties-martinelli.AKBL.desktop"
remove_file "/usr/share/applications/com.senties-martinelli.AKBL-indicator.desktop"
remove_file "/usr/share/applications/com.senties-martinelli.AKBL-windicator.desktop"
remove_file "/usr/share/applications/fr.rsm92.akbl.desktop"
remove_file "/usr/share/applications/fr.rsm92.akbl-indicator.desktop"
remove_file "/usr/share/applications/fr.rsm92.akbl-windicator.desktop"
remove_file "/usr/bin/akbl"
remove_file "/usr/lib/systemd/system/AKBL.service"
remove_dir  "/usr/share/AKBL"
remove_dir  "/usr/share/doc/AKBL"
remove_dir  "/usr/lib/python3/AKBL"
