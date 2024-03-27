#!/usr/bin/env bash
# bash <(curl -s https://pastebin.com/raw/DaWs3JMy)

set -euo pipefail

function cleanup {
        echo "Exiting script"

        # Undo the HTTPS setting
        git config --global --unset url."https://github.com/".insteadOf

        exit
}

trap cleanup EXIT

function die {
        printf 'Error: %s\n' "$@" 1>&2
        exit 1
}

# Ask for confirmation
while true; do
    echo ""
    echo "This script is intended for throwaway RPIs meant to run PiMatTimer from fresh install. So:"
    echo "- it will set your git config to use HTTPS and not SSH (for unauthenticated cloning)"
    echo "- it will globally install Python libraries, which is not recommended"
    echo "- it will run the timer on boot-up, so if something breaks, know how to ssh"
    echo ""
    read -p "Install? [y/n] " yn
    case "${yn}" in
        [Yy]* ) echo "Alright, let's roll"; break;;
        [Nn]* ) echo Bye; exit;;
        * ) echo "Please answer [y/n]";;
    esac
done

function install-lcd {
        local lcd_folder="LCD-show"
        local lcd_script="LCD35-show"
        [[ -d "./${lcd_folder}" ]] && die "LCD repo './${lcd_folder}' exists! Aborting"
        git clone https://github.com/goodtft/LCD-show.git
        chmod -R 755 "./${lcd_folder}"
        pushd -- "${lcd_folder}"
        sed -i '${/sudo reboot/d;}' "./${lcd_script}"
        sudo "./${lcd_script}"
        popd
}

INSTALL_DIR="${HOME}"
AUTOSTART_DIR="${HOME}/.config/autostart"
AUTOSTART_ENTRY="${AUTOSTART_DIR}/timer.desktop"

# cd to install dir and check if stuff is already installed
cd -- "${INSTALL_DIR}" || die "Could not cd to ${INSTALL_DIR}"
[[ -d "PiMatTimer" ]] && die "PiMatTimer exists at ${INSTALL_DIR}! Aborting"
[[ -f "${AUTOSTART_ENTRY}" ]] && die "Autostart entry at ${AUTOSTART_ENTRY} exists! Aborting"

# Ask if user wants to install drivers
while true; do
    echo ""
    echo "Install LCD35 drivers? [y] to install, [n] to skip this step"
    echo "- If you are not using LCD35 or already have them installed, choose [n]"
    echo ""
    read -p "Choice? [y/n] " yn
    case "${yn}" in
        [Yy]* ) install-lcd; break;;
        [Nn]* ) break;;
        * ) echo "Please answer [y/n]";;
    esac
done

# Install NodeJS
sudo apt -y install nodejs

# Use HTTPS instead of SSH by default
git config --global url."https://github.com/".insteadOf git@github.com:

# Clone repo and submodules
git clone https://github.com/mrusse/PiMatTimer --recurse-submodules

# Install dependencies
pushd -- PiMatTimer
python -m pip install -r requirements.txt --break-system-packages

# Export DISPLAY
[[ -v DISPLAY && "${DISPLAY}" == ':0.0' ]] || ( echo 'export DISPLAY=:0.0' >> ~/.bashrc )

# Make autostart entry
mkdir -p "${AUTOSTART_DIR}"
cat << EOF > "${AUTOSTART_ENTRY}"
[Desktop Entry]
Type=Application
Name=Timer
Exec=/usr/bin/python3 /home/pi/PiMatTimer/timer.py
EOF

echo "Success! Rebooting."
sudo reboot
