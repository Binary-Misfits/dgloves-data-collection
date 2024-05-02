import serial
import serial.tools.list_ports
import numpy as np
import os
import time
import keyboard

# Define function to create directories if they don't exist
def create_directories(label):
    directory = os.path.join('database', label)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

# Function to prompt for label
def prompt_for_label():
    return input("Enter label for recording: ")

# Function to get the next sample number in the directory
def get_next_sample_number(directory):
    files = os.listdir(directory)
    return len(files) + 1

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

record_data = False  # Flag to indicate whether to record data or not
start_time = 0  # Variable to store the start time of recording
label = None
samples_recorded = 0

while True:
    if keyboard.is_pressed('c') and not record_data:
        record_data = True
        if not label or samples_recorded in [0,30]:
            label = prompt_for_label()
            samples_recorded = 0
        print("Recording data...")
        data_buffer = []  # Buffer to store data during recording
        timestamp_buffer: list[float] = []  # Buffer to store timestamps during recording
        directory = create_directories(label)
        sample_number = get_next_sample_number(directory)
        start_time = time.time()  # Start time of recording
    
    if keyboard.is_pressed('x'):
        record_data = False
        if len(data_buffer) > 0:
            # Save the recorded data as a binary file
            timestamp_buffer = [(t - start_time) * 1000 for t in timestamp_buffer]  # Convert to milliseconds
            data_buffer_with_timestamp = np.column_stack((timestamp_buffer, data_buffer))
            filename = os.path.join(directory, f'sample_{sample_number}.npy')
            np.save(filename, data_buffer_with_timestamp)
            print(f"Recorded data saved to {filename}")
            sample_number += 1
            samples_recorded += 1
        else:
            print("No data recorded.")
        time.sleep(1)
    
    if keyboard.is_pressed('z'):
        record_data = False
        data_buffer = []
        timestamp_buffer = []
        print("Discarded Values!")
        time.sleep(1)
        
    if keyboard.is_pressed('q'):
        print("Exiting...")
        break

    if serialInst.in_waiting and record_data:
        packet = serialInst.readline()
        data = packet.decode('utf').rstrip('\n\r').split(',')
        data_buffer.append(data)
        timestamp_buffer.append(time.time())
