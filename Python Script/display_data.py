import serial
import serial.tools.list_ports
import numpy as np
import os
import time
import keyboard
import matplotlib.pyplot as plt

finger_data = [[] for _ in range(5)]
acc_data = [[] for _ in range(3)]
gyr_data = [[] for _ in range(3)]
timestamp_buffer = []

def visualize(data, start_time):
    
    finger_data.append(data[:5])
    acc_data.append(data[5:8])
    gyr_data.append(data[8:])
    timestamp_buffer.append(time.time()-start_time)
    
    # if len(finger_data) > 10:
    #     finger_data.pop(0)
    #     acc_data.pop(0)
    #     gyr_data.pop(0)
    #     timestamp_buffer.pop(0)
    
    # Extract finger data and plot
    for i in range(5):
        finger_data[i].append(int(data[i]))
        axs1.clear()
        axs1.set_title("Finger Data")
        axs1.set_xlabel("Time")
        axs1.set_ylabel("Value")
        for j in range(5):
            if finger_data[j] and len(timestamp_buffer) == len(finger_data[j]):
                axs1.plot(timestamp_buffer, finger_data[j], label=f"Finger {j+1}")
        axs1.legend()
    
    # Extract accelerometer data and plot
    for i in range(5, 8):
        acc_data[i-5].append(float(data[i]))
        axs2.clear()
        axs2.set_title("Accelerometer Data")
        axs2.set_xlabel("Time")
        axs2.set_ylabel("Value")
        for j in range(3):
            if acc_data[j] and len(timestamp_buffer) == len(acc_data[j]):
                axs2.plot(timestamp_buffer, acc_data[j], label=f"Axis {j+1}")
        axs2.legend()
    
    # Extract gyroscope data and plot
    for i in range(8, 11):
        gyr_data[i-8].append(float(data[i]))
        axs3.clear()
        axs3.set_title("Gyroscope Data")
        axs3.set_xlabel("Time")
        axs3.set_ylabel("Value")
        for j in range(3):
            if gyr_data[j] and len(timestamp_buffer) == len(gyr_data[j]):
                axs3.plot(timestamp_buffer, gyr_data[j], label=f"Axis {j+1}")
        axs3.legend()

# List available serial ports
ports = serial.tools.list_ports.comports()
portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: COM")

portVar = None
for x in range(0, len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)

if portVar is None:
    print("Invalid port selection. Exiting...")
    exit()

serialInst = serial.Serial(portVar, 9600)
record_data = False  # Flag to indicate whether to record data or not
start_time = None  # Variable to store the start time of recording
label = None
samples_recorded = 0

# Create a figure and three subplots
fig, (axs1, axs2, axs3) = None, (None, None, None)

while True:
    if keyboard.is_pressed('c') and not record_data:
        fig, (axs1, axs2, axs3) = plt.subplots(3, 1, figsize=(10, 10))
        record_data = True
        print("Starting Plot...")
        start_time = time.time()  # Start time of recording
        plt.ion()

    if keyboard.is_pressed('z'):
        record_data = False
        finger_data = [[] for _ in range(5)]
        acc_data = [[] for _ in range(3)]
        gyr_data = [[] for _ in range(3)]
        timestamp_buffer = []
        plt.close()
        print("Stopped Plotting!")
        time.sleep(1)

    if keyboard.is_pressed('q'):
        print("Exiting...")
        break

    if serialInst.in_waiting and record_data:
        packet = serialInst.readline()
        data = packet.decode('utf').rstrip('\n\r').split(',')
        
        visualize(data, start_time)

        plt.tight_layout()
        plt.draw()
        plt.pause(0.0001)

# Close serial connection
serialInst.close()
