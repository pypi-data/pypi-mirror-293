import os
import pandas as pd

def load_dataset():
    package_dir = os.path.dirname(__file__)
    dataset_file = os.path.join(package_dir, 'enjoysport.csv')
    return pd.read_csv(dataset_file)