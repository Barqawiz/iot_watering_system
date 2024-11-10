import PCF8591 as ADC
import time
from pump import start_motor, stop_motor

# Initialize PCF8591 at address 0x48
ADC.setup(0x48)

# 3V3 threshold
HIGH_VALUES = [173, 165]
WATERED_THRESHOLD = 135
WATER_MAX = 82

WAIT_DURATION = 10  # 10 seconds
DELAY_TIME = 0.6  # Delay 0.6 seconds for next reading
BREAK_TIME = 5

# Track watering status
watering_start_time = None
is_watering = False


# Define functions to handle each state
def need_water_or_not_in_soil():
    print("Status: soil is very dry or sensor is not in soil.")
    start_motor()
    global is_watering
    is_watering = True


def need_water():
    print("Status: plant needs water.")
    start_motor()
    global is_watering
    is_watering = True


def enough_water():
    print("Status: soil has enough water.")
    if is_watering:
        stop_motor()


def track_water_start_time():
    global watering_start_time
    watering_start_time = time.time()


try:
    while True:
        # If currently watering: bypass reading to avoid interference
        if is_watering:
            elapsed_time = time.time() - watering_start_time

            if elapsed_time >= WAIT_DURATION:
                # Stop the motor after watering time
                enough_water()
                is_watering = False
                watering_start_time = None
            else:
                # Still watering: skip readings
                time.sleep(DELAY_TIME)
                continue

            # Wait the voltage to adjust
            print("Finished watering - resetting readers")
            stop_motor()
            time.sleep(BREAK_TIME)

        # Read moisture level
        moisture_level = ADC.read(2)
        print(f"Current Moisture Level: {moisture_level}")

        # Determine watering levels
        if moisture_level < WATERED_THRESHOLD:
            enough_water()
        elif moisture_level in HIGH_VALUES:
            need_water()
            track_water_start_time()
        else:
            need_water_or_not_in_soil()
            track_water_start_time()

        time.sleep(DELAY_TIME)

except KeyboardInterrupt:
    # Exit on CTRL+C
    print("Exit")
    stop_motor()
