# Tutorial
This document contains a comprehensive tutorial on how to build your own Mynt.

## Materials
For building your own Mynt, you will need the following:
- **1x [Raspberry Pi Zero W](https://www.raspberrypi.org/pi-zero-w/)**
- **1x micro USB power chord** to power the RPI
- **1x micro SD (>= 3 GB)** + a way to plug it into your PC/laptop
- **5x WS281x LED diodes** (I use [WS2813](http://www.addressable-led.com/Products/WS2813-LED-Chip.html), but it shouldn't really matter)
- **1x [Pulse Sensor](https://pulsesensor.com/)** (or some knock-off version from Ebay)
- **1x ADS1115,** because RPI dones't do analog sensors
- **1x TTP223** Capacitive Touch switch
- **soldering equipment + wiring** to put it all together
- **3D-printed Mynt case**, although this is mostly aesthetical
	- TODO: link to model

## Software
First, plug the micro SD card to your computer, run `code/setup/setup.sh` and follow the instructions. When done, plug the micro SD to your Raspberry Pi (don't boot it just yet!) and you're done with the software part of the project.
