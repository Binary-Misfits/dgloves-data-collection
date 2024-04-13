import serial
import serial.tools.list_ports
import csv
import os
from datetime import datetime
import keyboard

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
    "timestamp", "fid1", "fid2", "fid3", "fid4","fid0",
    "axn", "ayn", "azn",
    "gxn", "gyn", "gzn","label"
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

    record_data = False  # Flag to indicate whether to record data or not

    while True:
        if keyboard.is_pressed('ctrl+r'):
            record_data = True
            print("Recording data...")
        
        if keyboard.is_pressed('ctrl+x'):
            record_data = False
            print("Discarding data...")

        if serialInst.in_waiting and record_data:
            packet = serialInst.readline()
            data = packet.decode('utf').rstrip('\n\r').split(',')
            timestamp = datetime.now().strftime('%H:%M:%S')
            row = [timestamp] + data
            writer.writerow(row)
            print(row)

