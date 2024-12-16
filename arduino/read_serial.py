import serial
import datetime
import time 

def read_serial_input(comport: str, baudrate: int = 9600, use_timestamp: bool = False):
    """
    Function to read sensor readings from the Arduino through a serial input connection.
    For example, if the Raspberry PI is connected to the Arduino through a USB cable.

    Parameters
    ==========
    comport : str 
        Name of the Serial interface of the Arduino

    baudrate : int
        Baudrate of the Arduino

    use_timestamp : bool
        Boolean flag to append timestamp to each reading received by the Raspberry PI
    """
    ser_port = serial.Serial(comport, baudrate, timeout=0.1)

    while True:
        data = ser_port.readline().decode().strip()
        if data and use_timestamp:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time}, {data}")
        elif data:
            print(data)
        time.sleep(1) 
            

if __name__ == "__main__":
    read_serial_input('COM28', 9600, True)
