#!/bin/bash
# To be copied to /home/pi/install.sh
# A script to be ran the first time RPI starts.
DEBUG=1

set -eu
cd "$(dirname "$0")"


# update, install apps
echo "Updating and installing packages."
apt-get update -y
apt-get upgrade -y

apt-get install git python3-pip -y
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
echo "Enabling MTP."
mv "rc.local" "/etc/rc.local"
chmod +x "/etc/rc.local"

mkdir -p "/etc/umtprd"
mv "umtprd.conf" "/etc/umtprd/umtprd.conf"

echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
git clone https://github.com/viveris/uMTP-Responder umtp
make -C umtp
sudo mv umtp/umtprd /usr/bin/umtprd


# i2c stuff
echo "Enabling i2c."
apt-get install i2c-tools -y

echo "i2c-bcm2708" | sudo tee -a /etc/modules
echo "i2c-dev" | sudo tee -a /etc/modules

echo "dtparam=i2c0=on" | sudo tee -a /boot/config.txt
echo "dtparam=i2c1=on" | sudo tee -a /boot/config.txt
echo "dtparam=i2c_arm=on" | sudo tee -a /boot/config.txt


# clean-up
echo "Cleaning up."
rm ~/install.sh
rm -r umtp

cat << EOF

Installation done!
EOF

reboot
