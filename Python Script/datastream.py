import serial
import serial.tools.list_ports
import csv
import os
from datetime import datetime

# Function to check and write the header if necessary
def check_and_write_header(csv_file_path, headings):
    file_exists = os.path.isfile(csv_file_path)
    if not file_exists:
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headings)

# Define CSV file path and headings
csv_file_path = 'data.csv'
headings = [
    "timestamp", "index", "middle", "ring", "piny",
    "Accelerometer Xraw", "Accelerometer Yraw", "Accelerometer Zraw",
    "Accelerometer Xnorm", "Accelerometer Ynorm", "Accelerometer Znorm",
    "Gyroscope Xraw", "Gyroscope Yraw", "Gyroscope Zraw",
    "Gyroscope Xnorm", "Gyroscope Ynorm", "Gyroscope Znorm","Category"
]

# Ensure header is written
check_and_write_header(csv_file_path, headings)

# List available serial ports
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: COM")

for x in range(0, len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)

serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

# Append data to the CSV file
with open(csv_file_path, mode='a', newline='') as file:
    writer = csv.writer(file)

    while True:
        if serialInst.in_waiting:
            packet = serialInst.readline()
            data = packet.decode('utf').rstrip('\n').split(',')
            timestamp = datetime.now().strftime('%H:%M:%S')
            row = [timestamp] + data
            writer.writerow(row)
            print(row)
