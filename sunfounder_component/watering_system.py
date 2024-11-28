import PCF8591 as ADC  # Import PCF8591 module
import time

from pump import start_motor, stop_motor

ADC.setup(0x48)  # Initialize PCF8591 at address 0x48

# Define threshold
# HIGH_VALUES = [100, 99, 65] # 5V
# WATERED_THRESHOLD = 50 # 5V

HIGH_VALUES = [173, 165] # 3V3
WATERED_THRESHOLD = 135 # 3V3
WATER_MAX = 82

WAIT_DURATION = 10  # 10 seconds watering time
DELAY_TIME = 0.6  # Delay next reading of 0.6 seconds

# Track watering status
previous_moisture_level = None
watering_start_time = None
is_watering = False


# Define functions to handle each state
def need_water_or_not_in_soil():
    print("Status: Soil is very dry or sensor is not in soil.")
    # TODO: implement motor/screen logic

    start_motor()


def need_water():
    print("Status: Soil is dry, the plant need water.")
    # TODO: implement motor/screen logic

    start_motor()


def being_watered():
    print("Status: Soil is currently being watered.")
    # TODO: implement motor/screen logic


def enough_water():
    print("Status: Soil has enough water.")
    # TODO: implement motor/screen logic

    stop_motor()


try:
    while True:  # Continuously read
        moisture_level = ADC.read(2)  # Read from Soil Moisture Sensor at AIN2
        print(f"Current Moisture Level: {moisture_level}")

        if not is_watering:
            if previous_moisture_level in HIGH_VALUES and (previous_moisture_level - moisture_level) >= 5:
                is_watering = True
                watering_start_time = time.time()
                being_watered()
            else:
                if moisture_level < WATERED_THRESHOLD:
                    enough_water()
                else:
                    need_water()
        else:
            if moisture_level <= WATERED_THRESHOLD:
                elapsed_time = time.time() - watering_start_time
                
                if elapsed_time >= WAIT_DURATION:
                    is_watering = False
                    watering_start_time = None
                    enough_water()
                else:
                    being_watered()
            else:
                being_watered()

        previous_moisture_level = moisture_level

        time.sleep(DELAY_TIME)

except KeyboardInterrupt:
    print("Exit")  # Exit on CTRL+C
    stop_motor()
except Exception as e:
    print("Error Exception: ", e) 
    stop_motor()
