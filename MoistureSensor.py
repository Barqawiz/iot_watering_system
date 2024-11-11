"""
This Raspberry Pi code was developed by newbiely.com
This Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-soil-moisture-sensor
"""


import time
import Adafruit_ADS1x15

# Create an ADS1115 ADC object
adc = Adafruit_ADS1x15.ADS1115(busnum=1)

# Set the gain to ±4.096V (adjust if needed)
GAIN = 1
THRESHOLD = 18000

# Main loop to read the analog value from the soil moisture sensor and print the raw ADC value
try:
    while True:
        # Read the raw analog value from channel A3
        raw_value = adc.read_adc(3, gain=GAIN)

        # Print the raw ADC value
        print("Raw Value: {}".format(raw_value))

        if raw_value > THRESHOLD:
            print("No Water")
        else:
            print("Water")

        # Add a delay between readings (adjust as needed)
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting the program.")