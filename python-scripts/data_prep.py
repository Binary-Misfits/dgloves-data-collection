import numpy as np
from pathlib import Path
import json
from sklearn.model_selection import train_test_split

class Dataset:
    """
    A class to handle loading and processing of a dataset containing numpy arrays,
    and to save the processed data as JSON.
    """

    __cwd = Path.cwd()

    def __init__(self, path: str, verbose: bool= False):
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
            for idx, sample in enumerate(label.iterdir()):
                arr = np.load(sample, allow_pickle=True).astype(float)[:,1:]
                
                # Duplicate and concatenate columns
                arr = np.concatenate([np.repeat(arr[:, i], 2) for i in range(arr.shape[1])], axis=1)
                
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
                
                if verbose:
                    print(f'Added sample: {idx + 1}')
            
            # Store padded arrays for each label
            self.raw[label.name] = np.stack(samples)
            if verbose:
                print(f'Samples for label {label} - Loaded!')
            
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
            
    def label_encodings(self):
        return {label: idx for idx, label in enumerate(set(self.raw.keys()))}
    
    def length(self, label: str | None =None):
        if label:
            if label not in self.raw.keys(): raise ValueError(f'provided label {label} does not exist in the dataset')
            
            return len(self.raw[label])
            
        return sum(len(data) for data in self.raw.values())
    
    def num_classes(self):
        return len(self.raw.keys())
    
    def split_data(self, test_size=0.2, validation_size=0.25, random_state:int =None):
        """
        Splits the dataset into training, validation, and test sets.

        Args:
        - test_size (float): Proportion of the dataset to include in the test split (default: 0.2).
        - validation_size (float): Proportion of the dataset to include in the validation split (default: 0.25).
        - random_state (int or None): Random state for shuffling the data (default: None).

        Returns:
        - train_data (tuple): Tuple containing a list of labels and a list of samples for training.
        - val_data (tuple): Tuple containing a list of labels and a list of samples for validation.
        - test_data (tuple): Tuple containing a list of labels and a list of samples for testing.
        """
        train_labels = []
        train_samples = []
        val_labels = []
        val_samples = []
        test_labels = []
        test_samples = []

        # Shuffle data for each label
        for label, data in self.raw.items():
            idx = np.arange(len(data))
            np.random.shuffle(idx)
            shuffled_data = data[idx]

            # Split shuffled data into train, validation, and test sets
            train, test = train_test_split(shuffled_data, test_size=test_size, random_state=random_state)
            train, val = train_test_split(train, test_size=validation_size, random_state=random_state)

            # Store split data for each label
            train_labels.extend([label] * len(train))
            train_samples.extend(train)
            val_labels.extend([label] * len(val))
            val_samples.extend(val)
            test_labels.extend([label] * len(test))
            test_samples.extend(test)

        return (train_labels, train_samples), (val_labels, val_samples), (test_labels, test_samples)

                
if __name__ == '__main__':
    # Create Dataset object
    dataset = Dataset('database')
    
    train, val, test = dataset.split_data()
    
    print(train[1][0])
    
    # Print the first element of the first array for labels 'l' and 'r'
    # print([(label, data.shape) for label, data in dataset.raw.items() if label in ['l', 'r']])
    
    # Save processed data as JSON
    # dataset.save_json('data.json')

    
