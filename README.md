# Raspberry-Pi-Projects
Wazza's Thermal Detector v1.0

This is my first Raspberry Pi project for the Pico.  

It's for detecting thermals on the ground for flying model aircraft.  The temp is displayed on the OLED display and there is a temp plotter with 4 deg c scale that is updated every second. You can see small rises in temp which may indicate a thermal coming. There is also an alarm that can be turned on and off which indicates fast rises or falls in temp. The range of the p[lotter is 4 deg c and will reset if the temp incerases or decreases by + or - 2 deg C.

The device nees to be small and is powered by a Lipo Battery. It can be attached to a streamer pole but the the temp sensor needs a shield around it to shade it from the sun.

It seems to work quite well.

Parts needed are: 

 - Raspberry Pi Pico H (with Headers) https://core-electronics.com.au/raspberry-pi-pico-h-with-headers.html
 - OLED Display Module for Raspberry Pi Pico, 1.3inch, SPI/I2C (64×128) https://core-electronics.com.au/oled-display-module-for-raspberry-pi-pico-1-3inch-spi-i2c-64-128.html
 - Maker Pi Pico Mini - Without Raspberry Pi Pico / Pico W (Pre-Soldered Pin Header) https://core-electronics.com.au/maker-pi-pico-mini-without-raspberry-pi-pico-pico-w-pre-soldered-pin-header.html
 - PiicoDev Precision Temperature Sensor TMP117 https://core-electronics.com.au/catalogsearch/result/?q=tmp117
 - Polymer Lithium Ion Battery (LiPo) 3.7V 1100mAh https://core-electronics.com.au/polymer-lithium-ion-battery-1000mah-38458.html

Install the piicodev package in Thonny by selecting Tools, Manage Packages, then search for Piicodev 
or you can Download the individual PiicoDev Libraries from https://github.com/CoreElectronics/CE-PiicoDev-PyPI 
