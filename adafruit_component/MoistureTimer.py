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
            now = datetime.now()
            raw_value = self.adc.read_adc(3, gain=self.GAIN)
            # raw_value = self.something
            # Print the raw ADC value
            print(str(now) + str(" Raw Value: {}".format(raw_value)), file=open(self.FILENAME, 'a'))

            # if raw_value > self.THRESHOLD:
            #     print("No Water", file=open(self.FILENAME, 'a'))
            # else:
            #     print("Water", file=open(self.FILENAME, 'a'))
        except KeyboardInterrupt:
            print("\nExiting the program.")


if __name__ == '__main__':
    moisture_timer = MoistureTimer("TestFiles/24HourTest.txt")
    moisture_timer.start()
    # time.sleep(30)
    # moisture_timer.stop()
