import PCF8591 as ADC  # Import PCF8591 module
import time
from datetime import datetime

from pump import start_motor, stop_motor

ADC.setup(0x48)  # Initialize PCF8591 at address 0x48

# Define threshold
# HIGH_VALUES = [100, 99, 65] # 5V
# WATERED_THRESHOLD = 50 # 5V

HIGH_VALUES = [173, 165]  # 3V3
WATERED_THRESHOLD = 130  # 3V3
WATER_MAX = 82

WAIT_DURATION = 5  # 5 seconds watering time
DELAY_TIME = 60 * 10  # Delay next reading 10 minutes

# Track watering status
previous_moisture_level = None
watering_start_time = None
is_watering = False

# log file
LOG_FILE = "watering_system.txt"


def log_reading(moisture_level, water_status):
    """Log the readings with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"- moisture_reading: {moisture_level}, time: {timestamp}, water_status: {water_status}, watering_threshold: {WATERED_THRESHOLD}.\n"
    with open(LOG_FILE, "a") as file:
        file.write(log_entry)


# Define functions to handle each state
def need_water_or_not_in_soil():
    print("Status: Soil is very dry or sensor is not in soil.")
    start_motor()


def need_water():
    print("Status: Soil is dry, the plant need water.")
    start_motor()


def being_watered():
    print("Status: Soil is currently being watered.")


def enough_water():
    print("Status: Soil has enough water.")
    stop_motor()
    global is_watering
    is_watering = False


try:
    while True:  # Continuously read
        moisture_level = ADC.read(2)  # Read from Soil Moisture Sensor at AIN2
        print(f"Current Moisture Level: {moisture_level}")

        if moisture_level < WATERED_THRESHOLD:
            water_status = "Enough Water"
            enough_water()
            log_reading(moisture_level, water_status)
            previous_moisture_level = moisture_level
            time.sleep(DELAY_TIME)
        else:
            water_status = "Need Water"
            need_water()
            log_reading(moisture_level, water_status)
            previous_moisture_level = moisture_level

            # Watering duration
            time.sleep(WAIT_DURATION)

            # Stop the motor and start new cycle
            stop_motor()

            water_status = "Enough Water"
            enough_water()
            log_reading(moisture_level, water_status)

except KeyboardInterrupt:
    print("Exit")  # Exit on CTRL+C
    stop_motor()
except Exception as e:
    error_message = f"Error Exception: {e}"
    print(error_message)
    with open(LOG_FILE, "a") as file:
        file.write(
            f"- error: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n"
        )
    stop_motor()
