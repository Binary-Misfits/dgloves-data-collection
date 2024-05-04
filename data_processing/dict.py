import os
import numpy as np

# Path to the folder containing .npy files
folder_path = 'Updated_Data'

# Initialize a dictionary to store data with labels as keys and arrays (samples) as values
data_dict = {}

# List all .npy files in the folder
file_names = [file for file in os.listdir(folder_path) if file.endswith('.npy')]

# Iterate over each .npy file
for file_name in file_names:
    # Extract label from the file name
    label = file_name.split('.')[0]  # Assuming the label is the file name without extension
    # Load data from the .npy file
    array_data = np.load(os.path.join(folder_path, file_name))
    # Update the dictionary with label as key and array (samples) as value
    data_dict.setdefault(label, []).append(array_data)

# Print the data dictionary
print(data_dict)
