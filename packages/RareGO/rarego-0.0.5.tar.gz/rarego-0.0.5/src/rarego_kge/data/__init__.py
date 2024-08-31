import os
import pandas as pd

# Define the path to the data directory
data_dir = os.path.join(os.path.dirname(__file__), 'data')

# Function to load dataset1
def R25KG-Rare():
    dataset1_path = os.path.join(data_dir, 'R25KG-Rare.csv')
    return pd.read_csv(dataset1_path)

# Function to load dataset2
def R25KG-Rare-Gene():
    dataset2_path = os.path.join(data_dir, 'R25KG-Rare-Gene.csv')
    return pd.read_csv(dataset2_path)

__all__ = [
    "R25KG-Rare",
    "R25KG-Rare-Gene",
    # You can add other functions or classes here as needed
]


# Load each dataset
#dataset1 = load_dataset1()
#dataset2 = load_dataset2()
