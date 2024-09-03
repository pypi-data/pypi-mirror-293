import pandas as pd
import csv
from typing import Dict, List

def read_csv(file_path: str) -> pd.DataFrame:
    """
    Read a CSV file and return a pandas DataFrame.
    """
    return pd.read_csv(file_path)

def write_csv(file_path: str, data: Dict[str, List]):
    """
    Write data to a CSV file.
    """
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        writer.writeheader()
        writer.writerows([{k: v[i] for k, v in data.items()} for i in range(len(next(iter(data.values()))))])

def merge_csv_by_plasmid_id(csv_paths: List[str], output_csv_path: str):
    data_frames = [pd.read_csv(csv_path, dtype={'plasmid_id': str}) for csv_path in csv_paths]
    merged_df = data_frames[0]
    for df in data_frames[1:]:
        merged_df = pd.merge(merged_df, df, on="plasmid_id", how='outer')
    merged_df['plasmid_id'] = merged_df['plasmid_id'].astype(str)  # Ensure plasmid_id is string
    merged_df.to_csv(output_csv_path, index=False)

# Add more data processing functions as needed