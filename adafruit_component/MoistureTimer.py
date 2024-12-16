import time
import Adafruit_ADS1x15
from ParentTimer import ParentTimer
from datetime import datetime


class MoistureTimer(ParentTimer):
    interval = 120  # sec
    def __init__(self, filename):
        # Create an ADS1115 ADC object
        self.adc = Adafruit_ADS1x15.ADS1115(busnum=1)
        # self.something = "something"

        # Set the gain to ±4.096V (adjust if needed)
        self.GAIN = 1
        self.THRESHOLD = 18000
        self.FILENAME = filename
        super().__init__()

    def timer(self):
        try:
            for gain in [16, 8, 4, 2, 1, 2 / 3]:
                # Add a delay between readings (adjust as needed)
                time.sleep(0.5)
                now = datetime.now()
                raw_value = self.adc.read_adc(3, gain=gain)
                # Print the raw ADC value
                print(str(now) + str(" RawValue{}: {}".format(gain, raw_value)), file=open(self.FILENAME, 'a'))
        except KeyboardInterrupt:
            print("\nExiting the program.")


if __name__ == '__main__':
    moisture_timer = MoistureTimer("TestFiles/ThirdLongTest.txt")
    moisture_timer.start()
    # time.sleep(30)
    # moisture_timer.stop()
