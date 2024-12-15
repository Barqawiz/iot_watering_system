import time
import Adafruit_ADS1x15
from ParentTimer import ParentTimer
from datetime import datetime
from bluedot.btcomm import BluetoothServer
from signal import pause
import re
import json

class MoistureTimer(ParentTimer):
    interval = 10  # sec
    gain1 = []
    gain2 = []
    gain23 = []
    def __init__(self, filename):
        # Create an ADS1115 ADC object
        self.adc = Adafruit_ADS1x15.ADS1115(busnum=1)
        # self.something = "something"

        # Set the gain to ±4.096V (adjust if needed)
        self.GAIN = 1
        self.THRESHOLD = 18000
        self.FILENAME = filename
        self.bluetoothServer = BluetoothServer(self.data_received)
        super().__init__()

    def timer(self):
        try:
            for gain in [2, 1, 2 / 3]:
                raw_sum = 0
                for count in [1, 2, 3, 4, 5]:
                    # Add a delay between readings (adjust as needed)
                    time.sleep(0.5)
                    now = datetime.now()
                    raw_sum += self.adc.read_adc(3, gain=gain)
                    # Print the raw ADC value
                raw_value = raw_sum/5
                print(str(now) + str(",RawValue{},{}".format(gain, raw_value)), file=open(self.FILENAME, 'a'))
                if gain == 1:
                    self.gain1.append([str(now.isoformat()), raw_value])
                elif gain == 2:
                    self.gain2.append([str(now.isoformat()), raw_value])
                else:
                    self.gain23.append([str(now.isoformat()), raw_value])
        except KeyboardInterrupt:
            print("\nExiting the program.")

    def data_received(self, data):
        print("Received request for data")
        try:
            chunk_size = 10
            if "Gain23" in data:
                chunks = [self.gain23[i:i + chunk_size] for i in range(0, len(self.gain1), chunk_size)]
                json_chunks = [json.dumps(chunk) for chunk in chunks]
                for i, chunk in enumerate(json_chunks):
                    self.bluetoothServer.send(chunk)
                self.bluetoothServer.send("complete")
            elif "Gain2" in data:
                chunks = [self.gain2[i:i + chunk_size] for i in range(0, len(self.gain1), chunk_size)]
                json_chunks = [json.dumps(chunk) for chunk in chunks]
                for i, chunk in enumerate(json_chunks):
                    self.bluetoothServer.send(chunk)
                self.bluetoothServer.send("complete")
            else:
                chunks = [self.gain1[i:i + chunk_size] for i in range(0, len(self.gain1), chunk_size)]
                json_chunks = [json.dumps(chunk) for chunk in chunks]
                for i, chunk in enumerate(json_chunks):
                    self.bluetoothServer.send(chunk)
                self.bluetoothServer.send("complete")
        except KeyboardInterrupt:
            print("\nExiting the program.")

    def parse_file(self):
        # Open the file in read mode
        with open('example.txt', 'r') as file:
            # Read all the lines from the file
            lines = file.readlines()

        # Loop through each line
        for line_number, line in enumerate(lines, start=1):
            # Remove leading and trailing whitespace (like \n, \t)
            cleaned_line = line.strip()
            values = re.findall(r',', cleaned_line)
            if values[1] == "RawValue1":
                self.gain1.append([values[0], values[2]])
            elif values[1] == "RawValue2":
                self.gain2.append([values[0], values[2]])
            else:
                self.gain23.append([values[0], values[2]])


if __name__ == '__main__':
    moisture_timer = MoistureTimer("TestFiles/BluetoothLongTest1.txt")
    moisture_timer.start()
    # time.sleep(30)
    # moisture_timer.stop()
