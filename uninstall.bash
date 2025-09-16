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
	echo -e "\n\033[0;32m Disabling the systemd daemon...\033[0m"
    systemctl stop akbl
    systemctl disable akbl
    echo ""
fi

echo -e "\033[0;32m Removing the python links..\033[0m"

AKBL_PYTHON_VERSIONS=("$(ls /usr/lib/ | grep python3)")

for python_version in "${AKBL_PYTHON_VERSIONS[@]}"; do

  if [[ "$python_version" != "python3" ]]; then

    if [[ -L "/usr/lib/$python_version/AKBL" ]]; then
      rm -f "/usr/lib/$python_version/AKBL" && echo -e "/usr/lib/$python_version/AKBL link removed"
    fi

    if [ -f "/usr/lib/$python_version/AKBL" ] || [ -f "/usr/lib/$python_version/AKBL.py" ]; then
        rm -f "/usr/lib/$python_version/AKBL" && echo -e "/usr/lib/$python_version/AKBL file removed"
    fi

    if [ -d "/usr/lib/$python_version/AKBL" ] || [ -d "/usr/lib/$python_version/AKBL.py" ]; then
        rm -rf "/usr/lib/$python_version/AKBL.py" && echo -e "/usr/lib/$python_version/AKBL directory removed"
    fi

  fi
    
done
echo ""



echo -e "\033[0;32m Removing the software files and directories..\033[0m"


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
remove_file "/usr/bin/akbl"
remove_file "/usr/lib/systemd/system/AKBL.service"
remove_dir  "/usr/share/AKBL"
remove_dir  "/usr/share/doc/AKBL"
remove_dir  "/usr/lib/python3/AKBL"
