import PCF8591 as ADC  # Import PCF8591 module
import time  # Import time for delay

ADC.setup(0x48)  # Initialize PCF8591 at address 0x48

try:
    while True:  # Continuously read and print moisture level
        print(ADC.read(2))  # Read from Soil Moisture Sensor at AIN1
        time.sleep(0.2)  # Delay of 0.2 seconds
except KeyboardInterrupt:
    print("Exit")  # Exit on CTRL+C
