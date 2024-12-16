import socket
import datetime
from time import (
    localtime
)
from hashlib import md5

from pathlib import Path
import os
import csv

UDP_IP = "IP ADDRESS GOES HERE"
UDP_PORT = 13900
BASE_FILENAME = "sensorlogs"
BASE_PATH = Path(os.getcwd()) / "logs"


def random_file_preamble(filename: str) -> str:
    """
    Helper function to create random strings to append to sensor log files.

    Parameter
    =========
    filename : str
        Base name of the file to append random hexstring.
    """
    suffix_ = md5(str(localtime()).encode("utf-8")).hexdigest()
    return f"{filename}_{suffix_}.csv"


def main():
    # Set up the Web Socket to receive incoming packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    full_filepath = BASE_PATH / random_file_preamble(BASE_FILENAME)
    try:
        sock.bind((UDP_IP, UDP_PORT))
    except socket.error as e:
        print(str(e))

    # Create a new CSV file to record packet information
    with open(full_filepath, "w", newline="") as csvfile:
        fieldnames = ["timestamp", "moisture_reading"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            # Decode the incoming packets
            data, addr = sock.recvfrom(2048)
            data_str = data.decode("utf-8")

            try:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Write reading to CSV File
                writer.writerow({"timestamp": current_time, "moisture_reading": data_str})
                print(f"Data received: {current_time} - {data_str}")
            except:
                print(f"Invalid value, data: {data_str}, Address: {addr}")

            if not data:
                print("No new data")
                break

if __name__ == "__main__":
    main()

