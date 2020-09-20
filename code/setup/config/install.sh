#!/bin/bash
# To be copied to /home/pi/install.sh
# A script to be ran the first time RPI starts.
DEBUG=1

set -eu
cd "$(dirname "$0")"

# update, install apps
apt-get update -y
apt-get upgrade -y

apt install git python3-pip -y
pip3 install \
	pyyaml \
	typeguard \
	rpi_ws281x \
	adafruit-circuitpython-neopixel \
	adafruit-circuitpython-ads1x15

if [ $DEBUG -eq 1 ]
then
	apt install vim tmux -y
fi

# set up (u)MTP
mv "rc.local" "/etc/rc.local"
chmod +x "/etc/rc.local"

mkdir -p "/etc/umtprd"
mv "umtprd.conf" "/etc/umtprd/umtprd.conf"

echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
git clone https://github.com/viveris/uMTP-Responder umtp
make -C umtp
sudo mv umtp/umtprd /usr/bin/umtprd

cat << EOF

Installation done!
EOF

reboot
