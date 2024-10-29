# Final Project
Watering system


## Capacitive Soil Moisture Module

### Components Used

- Raspberry Pi 5
- Capacitive Soil Moisture Module
- PCF8591 ADC/DAC Converter Module

[Component Setup Reference](https://docs.sunfounder.com/projects/umsk/en/latest/05_raspberry_pi/pi_lesson02_soil_moisture.html)

### Moisture Sensor Testing


I tested the soil moisture sensor in various conditions, and here are the initial range observations for 5V power:

- Sensor outside water and soil: 104 to 107
- Sensor in a cup of water: 45 to 48
- Sensor partially wet (removing from water): 75 to 98
- Sensor in slightly dry soil: 76 to 77
- Immediately after watering the soil: 48
- A short time after watering the soil: 52

For 3v3 power:

- Sensor outside water and soil: 173
- Sensor in a cup of water: 73
- Immediately after watering the soil: 80
- A short time after watering the soil: 110 

When using 3v3 power the range increases by 31 points
