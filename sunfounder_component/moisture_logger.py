import PCF8591 as ADC
import time
from datetime import datetime

# PCF8591 at address 0x48
ADC.setup(0x48)

# thresholds
WATERED_THRESHOLD = 135
DRY_THRESHOLD = 165

# log file
LOG_FILE = "moisture_log.txt"

def get_water_status(moisture_level):
    """Determine water status based on moisture level."""
    if moisture_level < WATERED_THRESHOLD:
        return "Enough Water"
    elif WATERED_THRESHOLD <= moisture_level < DRY_THRESHOLD:
        return "Need Water"
    else:
        return "Dry"

def log_reading(moisture_level, water_status):
    """Log the readings with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"- moisture_reading: {moisture_level}, time: {timestamp}, water_status: {water_status}, watering_threshold: {WATERED_THRESHOLD}.\n"
    with open(LOG_FILE, "a") as file:
        file.write(log_entry)

try:
    while True:
        # read moisture level
        moisture_level = ADC.read(2) 
        water_status = get_water_status(moisture_level)  # Get water status

        # display
        print(f"Moisture Reading: {moisture_level}, Status: {water_status}")
        log_reading(moisture_level, water_status)

        time.sleep(30)
except KeyboardInterrupt:
    print("Exiting program...")
