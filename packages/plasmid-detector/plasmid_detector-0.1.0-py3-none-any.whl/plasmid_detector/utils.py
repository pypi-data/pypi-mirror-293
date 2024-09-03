import os
import pandas as pd
from typing import List, Dict

def ensure_dir(directory: str):
    """
    Ensure that a directory exists, creating it if necessary.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.
    """
    return pd.read_csv(file_path)

def save_results(results: List[Dict], output_file: str):
    """
    Save analysis results to a CSV file.
    """
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)

# Add more utility functions as needed