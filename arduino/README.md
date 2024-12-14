# Arduino-based Soil Moisture Sensor

This sub-folder contains code for an Arduino-based solution for measuring the soil moisture levels.
The _Capacitive Soil Moisture V1.2._ is connected to an __Arduino UNO R4 Wifi__, and reads the analog
inputs from the sensor directly.

The __Arduino__ then transmits the sensor readings to a __Raspberry Pi 5__ using Wi-fi. The __Pi__ reads in the sensor readings
using a `socket`, and then stores the collected readings in a CSV file.
