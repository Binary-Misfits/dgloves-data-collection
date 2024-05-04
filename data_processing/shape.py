import os
import numpy as np

# Path to the folder containing .npy files
folder_path = 'database\\space'

# List all .npy files in the folder
file_names = [file for file in os.listdir(folder_path) if file.endswith('.npy')]

# Initialize max_shape with None
max_shape = None

# Iterate over each .npy file
for file_name in file_names:
    # Construct the full path to the .npy file
    file_path = os.path.join(folder_path, file_name)
    
    # Load the .npy array
    array_data = np.load(file_path)
    
    # Update max_shape
    if max_shape is None:
        max_shape = array_data.shape
    else:
        max_shape = tuple(np.maximum(max_shape, array_data.shape))

# Print the maximum shape
print("Maximum shape among all arrays:")
print(max_shape)
