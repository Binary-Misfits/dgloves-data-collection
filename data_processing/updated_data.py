import os
import numpy as np

# Path to the main folder containing subfolders with .npy files
main_folder_path = 'database'

# Path to the folder where padded .npy files will be saved
output_folder = 'Updated_Data'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Initialize a dictionary to store data with labels as keys and arrays (samples) as values
data_dict = {}

# Iterate over each subfolder in the main folder
for subfolder in os.listdir(main_folder_path):
    subfolder_path = os.path.join(main_folder_path, subfolder)
    # Check if it's a directory
    if os.path.isdir(subfolder_path):  
        # List all .npy files in the subfolder
        file_names = [file for file in os.listdir(subfolder_path) if file.endswith('.npy')]
        for file_name in file_names:
            file_path = os.path.join(subfolder_path, file_name)
            # Load data from the .npy file
            array_data = np.load(file_path)
            # Update the dictionary with label as key and array (samples) as value
            data_dict.setdefault(subfolder, []).append(array_data)

# Iterate over the dictionary and save each array (sample) to a separate .npy file
for label, arrays in data_dict.items():
    for i, array in enumerate(arrays):
        padded_array = np.zeros((375, 12))
        padded_array[:min(array.shape[0], 375), :min(array.shape[1], 12)] = array[:375, :12]
        output_file_path = os.path.join(output_folder, f'{label}_sample_{i}.npy')
        np.save(output_file_path, padded_array)

print("Padded data saved to:", output_folder)
