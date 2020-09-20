#!/bin/bash
# A script to set up RPI OS with Mynt on a specified device.
DEBUG=1

set -eu
cd "$(dirname "$0")"  # work relative to this script

RPI_BOOT_MNT_LOCATION=/tmp/rpimnt/boot
RPI_SYSTEM_MNT_LOCATION=/tmp/rpimnt/system

RPI_IMAGE_NAME=rpios.img
RPI_IMAGE_URL="https://downloads.raspberrypi.org/raspios_lite_armhf_latest"

ID_LENGTH=16

cat << EOF
Running Mynt configuration script.
----------------------------------
EOF

# download the RPI image (if it's not already downloaded)
if [ ! -f $RPI_IMAGE_NAME ]
then
	echo "$RPI_IMAGE_NAME not found, downloading the latest RPI OS."
	wget -q --show-progress $RPI_IMAGE_URL
	unzip raspios_lite_armhf_latest
	rm raspios_lite_armhf_latest
	mv *.img $RPI_IMAGE_NAME
fi

echo -n "Disk location (probably /dev/sdb or /dev/sdc): "; read disk

echo "Imaging $disk."
sudo mkfs.vfat $disk -I
sudo dd if=$RPI_IMAGE_NAME of=$disk status=progress

# copy instalation files over to the RPI
mkdir -p $RPI_BOOT_MNT_LOCATION $RPI_SYSTEM_MNT_LOCATION

sudo mount $disk\1 $RPI_BOOT_MNT_LOCATION
sudo mount $disk\2 $RPI_SYSTEM_MNT_LOCATION


echo "Saving Wifi credentials."
echo -n "Name: "; read name
echo -n "Password: "; read password
sudo tee $RPI_BOOT_MNT_LOCATION/wpa_supplicant.conf << EOF
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
	ssid="$name"
	psk="$password"
	scan_ssid=1
}
EOF


echo -n "Enter Mynt pair ID (leave empty to generate one): "; read id
if [ "$(echo $id | tr -d ' ')" == "" ]
then
	id=$(cat /dev/random | tr -cd a-zA-Z0-9 | head -c $ID_LENGTH)
	echo "ID: $id"
	echo "Enter it when creating the paired device. Press enter to continue."
	read
fi


echo "Copying configuration."
sudo cp -r config/* $RPI_SYSTEM_MNT_LOCATION/home/pi/

# create a file exposed to the user via MTP
sudo mkdir $RPI_SYSTEM_MNT_LOCATION/home/pi/mtp
sudo tee "$RPI_SYSTEM_MNT_LOCATION/home/pi/mtp/config.txt" << EOF
#----------------------------------------#
# This is a configuration file for Mynt. #
# It's YAML, but txt is user-friendly :) #
#----------------------------------------#

wifi:
- {name: "$name", password: "$password"}
#- {name: "wifi 2 name", password: "wifi 2 password"}  # another Wifi that Mynt will try next
#- {name 3: "wifi 3 name"}  # yet another Wifi, but this time without password

id: $id
EOF

sudo tee "$RPI_SYSTEM_MNT_LOCATION/etc/rc.local" << EOF
#!/bin/bash
/home/pi/install.sh | awk '{ print strftime("%c: "), $0; fflush(); }' | /home/pi/install.log &
exit 0
EOF
sudo chmod +x "$RPI_SYSTEM_MNT_LOCATION/etc/rc.local"


echo "Copying Mynt software."
sudo cp -r ../client $RPI_SYSTEM_MNT_LOCATION/home/pi/


if [ $DEBUG -eq 1 ]
then
	echo "[DEBUG] Enabling SSH."
	sudo touch $RPI_BOOT_MNT_LOCATION/ssh

	if [ -f ~/.ssh/id_rsa.pub ]
	then
		echo "[DEBUG] Copying ~/.ssh/id_rsa.pub to RPI's authorized keys."
		sudo mkdir -p $RPI_SYSTEM_MNT_LOCATION/home/pi/.ssh
		sudo cp ~/.ssh/id_rsa.pub $RPI_SYSTEM_MNT_LOCATION/home/pi/.ssh/authorized_keys
		sudo chmod 600 $RPI_SYSTEM_MNT_LOCATION/home/pi/.ssh/authorized_keys
	fi
fi

sleep 1
sudo umount $RPI_BOOT_MNT_LOCATION
sudo umount $RPI_SYSTEM_MNT_LOCATION

cat << EOF

Done!
Plug the SD into the Raspberry Pi Zero for it to get configured.
EOF
