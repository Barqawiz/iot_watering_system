# Arduino-based Soil Moisture Sensor

This sub-folder contains code for an Arduino-based solution for measuring the soil moisture levels.
The _Capacitive Soil Moisture V1.2._ is connected to an __Arduino UNO R4 Wifi__, and reads the analog
inputs from the sensor directly.

The __Arduino__ then transmits the sensor readings to a __Raspberry Pi 5__ using Wi-fi. The __Pi__ reads in the sensor readings
using a `socket`, and then stores the collected readings in a CSV file in a `logs` sub-directory.

## Collecting Moisture Readings

To collect moisture readings from the Arduino, check that both the Raspberry PI and the Arduino are connected to the same internet connection. Next, retrive the 
IP address of the Raspberry PI. While the Arduino is powered and collecting moisture readings, run `read_wifi.py` to receive the moisture readings on the Raspberry PI.

## Plotly Dashboard

After collecting moisture readings, the `arduino_dashboard.py` file creates a Plotly Dash visualization of the moisture readings over time, along with the underlying table of records. After installing the necessary libraries, run it with the command:

``python arduino_dashboard.py``
 