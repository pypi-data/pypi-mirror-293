import pytest
import pandas as pd
import os
from plasmid_detector.data_processor import read_csv, write_csv, merge_csv_by_plasmid_id

@pytest.fixture
def sample_data():
    return {
        'plasmid_id': [1, 2, 3],
        'sequence': ['ATCG', 'GCTA', 'TGCA']
    }

def test_read_csv(tmp_path):
    # Create a temporary CSV file
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    file_path = tmp_path / "test.csv"
    df.to_csv(file_path, index=False)
    
    # Test reading the CSV file
    result = read_csv(file_path)
    assert isinstance(result, pd.DataFrame)
    assert result.equals(df)

def test_write_csv(tmp_path, sample_data):
    file_path = tmp_path / "test_output.csv"
    write_csv(file_path, sample_data)
    
    # Check if the file was created and contains correct data
    assert os.path.exists(file_path)
   
    df = pd.read_csv(file_path, dtype={'plasmid_id': int})
    expected_df = pd.DataFrame(sample_data)
    expected_df['plasmid_id'] = expected_df['plasmid_id'].astype(int)
    assert df.equals(expected_df)

def test_merge_csv_by_plasmid_id(tmp_path):
    # Create sample CSV files
    df1 = pd.DataFrame({'plasmid_id': ['1', '2'], 'seq': ['ATCG', 'GCTA']})
    df2 = pd.DataFrame({'plasmid_id': ['1', '2'], 'length': [4, 4]})
    
    file1 = tmp_path / "file1.csv"
    file2 = tmp_path / "file2.csv"
    df1.to_csv(file1, index=False)
    df2.to_csv(file2, index=False)
    
    output_file = tmp_path / "merged.csv"
    merge_csv_by_plasmid_id([file1, file2], output_file)
    
    # Check if the merged file was created and contains correct data
    assert os.path.exists(output_file)
    result = pd.read_csv(output_file, dtype={'plasmid_id': str})
    expected = pd.merge(df1, df2, on='plasmid_id')
    expected['plasmid_id'] = expected['plasmid_id'].astype(str)  # Ensure expected df has string plasmid_id
    print("Result dtypes:", result.dtypes)
    print("Expected dtypes:", expected.dtypes)
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)  # Ignore dtype differences