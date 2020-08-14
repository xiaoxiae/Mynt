#!/bin/bash
# A script to set up RPI OS with Mynt on a specified device.
DEBUG=0

set -eu
cd "$(dirname "$0")"

RPI_BOOT_MNT_LOCATION=/tmp/rpimnt/boot
RPI_SYSTEM_MNT_LOCATION=/tmp/rpimnt/system

RPI_IMAGE_NAME=rpios.img
RPI_IMAGE_URL="https://downloads.raspberrypi.org/raspios_lite_armhf_latest"


echo "Running Mynt configuration script."
echo "----------------------------------"

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

# copy configuration files and an install script over to the PI
echo "Copying configuration."
sudo cp -r config/* $RPI_SYSTEM_MNT_LOCATION/home/pi/
sudo tee "$RPI_SYSTEM_MNT_LOCATION/etc/rc.local" << EOF
#!/bin/bash
/home/pi/install.sh &
exit 0
EOF
sudo chmod +x "$RPI_SYSTEM_MNT_LOCATION/etc/rc.local"

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

if [ $DEBUG -eq 1 ]
then
	echo "[DEBUG] Enabling SSH."
	sudo touch $RPI_BOOT_MNT_LOCATION/ssh
fi

sleep 1
sudo umount $RPI_BOOT_MNT_LOCATION
sudo umount $RPI_SYSTEM_MNT_LOCATION

echo ""
echo "Done!"
echo "Plug the SD into the Raspberry Pi Zero for it to get configured."

