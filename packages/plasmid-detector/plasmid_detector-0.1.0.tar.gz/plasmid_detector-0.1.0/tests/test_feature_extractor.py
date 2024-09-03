import pytest
from plasmid_detector.feature_extractor import (
    extract_basic_info,
    count_base_consecutive,
    count_pattern_occurrences,
    count_rich_regions,
    extract_features
)

@pytest.fixture
def sample_sequence():
    return "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG"

def test_extract_basic_info(sample_sequence):
    result = extract_basic_info(sample_sequence)
    assert result['length'] == 40
    assert result['gc_content'] == 0.5

def test_count_base_consecutive(sample_sequence):
    result = count_base_consecutive(sample_sequence, 2, 4)
    assert result['A_consecutive_2'] == 0
    assert result['T_consecutive_2'] == 0
    assert result['C_consecutive_2'] == 0
    assert result['G_consecutive_2'] == 0
    assert 'A_consecutive_4' not in result

def test_count_pattern_occurrences(sample_sequence):
    result = count_pattern_occurrences(sample_sequence, 2, 5)
    assert result['AT_count'] == 10
    assert result['CG_count'] == 10
    assert 'AA_count' not in result

def test_count_rich_regions(sample_sequence):
    result = count_rich_regions(sample_sequence, 10, 0.6)
    print("AT-rich regions:", result['at_rich_regions'])  # Add this line for debugging
    print("GC-rich regions:", result['gc_rich_regions'])  # Add this line for debugging
    assert result['at_rich_regions'] == 0
    assert result['gc_rich_regions'] == 0

def test_extract_features(sample_sequence):
    result = extract_features(sample_sequence)
    assert 'length' in result
    assert 'gc_content' in result
    assert 'A_consecutive_6' in result
    assert 'AT_count' in result
    assert 'ATC_count' in result
    assert 'ATCG_count' in result
    assert 'at_rich_regions' in result
    assert 'gc_rich_regions' in result