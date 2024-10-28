import PCF8591 as ADC  # Import PCF8591 module
import time

ADC.setup(0x48)  # Initialize PCF8591 at address 0x48

# Define threshold 
HIGH_VALUE = 100
SLIGHTLY_DRY_UPPER = 99
SLIGHTLY_DRY_LOWER = 56
WATERED_THRESHOLD = 48
WATERING_DURATION = 30  # seconds

# Initialize variables to track watering status
watering_start_time = None

# Define functions to handle each state
def need_water_or_not_in_soil():
    print("Status: Soil is very dry or sensor is not in soil. Action needed.")
    # TODO: implement the motor/screen logic

def need_water():
    print("Status: Soil is slightly dry. Monitoring.")
    # TODO: implement the motor/screen logic

def being_watered():
    print("Status: Soil is currently being watered.")
    # TODO: implement the motor/screen logic

def enough_water():
    print("Status: Soil has enough water. Monitoring.")
    # TODO: implement the motor/screen logic

try:
    while True:  # Continuously read and print moisture level
        moisture_level = ADC.read(2)  # Read from Soil Moisture Sensor at AIN2
        print(f"Current Moisture Level: {moisture_level}")
        
        # Check conditions for soil moisture levels
        if moisture_level >= HIGH_VALUE:
            need_water_or_not_in_soil()
        elif SLIGHTLY_DRY_LOWER <= moisture_level <= SLIGHTLY_DRY_UPPER:
            need_water()
        elif SLIGHTLY_DRY_LOWER >= moisture_level > WATERED_THRESHOLD:
            # Start the watering process if moisture level decreases
            if watering_start_time is None:
                watering_start_time = time.time()
            being_watered()
        elif moisture_level <= WATERED_THRESHOLD:
            # Continue watering if within the duration
            if watering_start_time and (time.time() - watering_start_time <= WATERING_DURATION):
                being_watered()
            else:
                # Reset watering status
                watering_start_time = None
                enough_water()

        time.sleep(0.6)  # Delay of 0.6 seconds

except KeyboardInterrupt:
    print("Exit")  # Exit on CTRL+C