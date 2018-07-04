# ANT+ App
Repository on getting the Power 2 Max power meter connected to the ant+ garmin usb dongle and writing data to the command line.

# Getting Started
Essentially follows the installation of the [ant-plus library](https://github.com/Loghorn/ant-plus) on javascript. However, the following are the steps that I took to get it working.

## Windows
### Installation of ANT+ USB 
1.  Download [Zadig](https://zadig.akeo.ie/) and install it
2.  Plug in your ant+ dongle into a USB port
3.  Open up Zadig
4.  Go into Options -> List All Devices
5.  Select ANT USB-m Stick as the selected USB driver
6.  Reinstall the driver to WinUSB

## Linux
1. Make sure you have the latest node.js and npm libraries
2. Run `sudo apt-get install build-essential libudev-dev` to install necessary files for the ant-plus nodejs library
3. Find the vendor and product ID by running the command `lsusb`. 

Example output:
```
Bus 005 Device 005: ID 0fcf:1009 Dynastream Innovations, Inc. ANTUSB-m Stick
```
In this example, it tells us that the vendor ID is 0fcf and the product ID is 1009 of the USB

4. Create a new udev rule
```
sudo vi /etc/udev/rules.d/ant-usb-m.rules
```
This will open up the vi text editor and create a file at that location

5. Put the following into the rules file
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fcf", ATTRS{idProduct}=="1009", RUN+="/sbin/modprobe usbserial vendor=0x0fcf product=0x1009", MODE="0666", OWNER="pi", GROUP="root"
```

6. Check that the system identifies the new USB
```
ls /dev/ttyUSB0
```
The console should output `/dev/ttyUSB0`

7. Unplug the USB and run the script by typing `node index.js`

