import numpy as np
from pathlib import Path
import json

class Dataset:
    """
    A class to handle loading and processing of a dataset containing numpy arrays,
    and to save the processed data as JSON.
    """

    __cwd = Path.cwd()

    def __init__(self, path: str):
        """
        Initializes the Dataset object.

        Args:
        - path (str): Relative path to the dataset directory.

        Attributes:
        - data_path (Path): Path to the dataset directory.
        - raw (dict): Dictionary to store raw data with labels as keys and numpy arrays as values.
        - max_length (int): Maximum length of arrays in the dataset.
        """
        self.data_path = self.__cwd.joinpath(path)
        self.raw: dict[str, np.ndarray[np.ndarray]] = dict()

        # Find the maximum length of arrays in the dataset
        self.max_length = max([max([np.load(item, allow_pickle=True).shape[0] for label_path in self.data_path.iterdir() for item in label_path.iterdir()])])
        
        # Load and pad arrays for each label in the dataset
        for label in self.data_path.iterdir():
            samples = []
            for sample in label.iterdir():
                arr = np.load(sample, allow_pickle=True).astype(float)[:,1:]
                
                # Min-max normalization except for the timestamp feature
                min_vals = np.min(arr, axis=0)
                max_vals = np.max(arr, axis=0)
                
                # Handle division by zero
                max_vals[max_vals == min_vals] += 1e-8
                
                # MinMax normalization
                normalized_arr = np.copy(arr)
                normalized_arr = (arr - min_vals) / (max_vals - min_vals)
                
                padded_arr = np.pad(normalized_arr, ((0, self.max_length - arr.shape[0]), (0, 0)), mode='constant')
                samples.append(padded_arr)
            
            # Store padded arrays for each label
            self.raw[label.name] = np.stack(samples)
            
    def save_json(self, path: str):
        """
        Saves the processed data as JSON.

        Args:
        - path (str): Relative path to save the JSON file.
        """
        # Convert numpy arrays to lists for JSON serialization
        formated_data = {label: data.tolist() for label, data in self.raw.items()}
        # Write formatted data to JSON file
        with open(path, 'w+') as json_file:
            json.dump(formated_data, json_file)
                
if __name__ == '__main__':
    # Create Dataset object
    dataset = Dataset('database')
    
    print([(label, data) for label, data in dataset.raw.items() if label in ['l', 'r']])
    
    # Print the first element of the first array for labels 'l' and 'r'
    # print([(label, data.shape) for label, data in dataset.raw.items() if label in ['l', 'r']])
    
    # Save processed data as JSON
    # dataset.save_json('data.json')

    