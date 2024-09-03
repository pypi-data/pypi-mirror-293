import pandas as pd
import numpy as np
from typing import Dict, List
import re
import itertools

def extract_basic_info(sequence: str) -> Dict[str, float]:
    """
    Extract basic information from a DNA sequence.
    """
    length = len(sequence)
    gc_content = (sequence.count('G') + sequence.count('C')) / length
    return {"length": length, "gc_content": gc_content}

def count_base_consecutive(sequence: str, min_length: int, max_length: int) -> Dict[str, int]:
    """
    Count consecutive occurrences of bases in a DNA sequence.
    """
    bases = "ATGC"
    counts = {}
    for base in bases:
        for length in range(min_length, max_length):
            key = f"{base}_consecutive_{length}"
            counts[key] = len([m.start() for m in re.finditer(f'{base}{{{length},}}', sequence)])
    return counts

def count_pattern_occurrences(sequence: str, pattern_length: int, min_count: int) -> Dict[str, int]:
    """
    Count occurrences of DNA patterns of a specific length.
    """
    patterns = [''.join(p) for p in itertools.product("ATGC", repeat=pattern_length)]
    counts = {}
    for pattern in patterns:
        count = sum(1 for _ in re.finditer(f'(?={pattern})', sequence))
        if count >= min_count:
            counts[f"{pattern}_count"] = count
    return counts

def count_rich_regions(sequence: str, window_size: int, threshold: float) -> Dict[str, int]:
    at_count = 0
    gc_count = 0
    for i in range(len(sequence) - window_size + 1):
        window = sequence[i:i+window_size]
        at_content = (window.count('A') + window.count('T')) / window_size
        gc_content = (window.count('G') + window.count('C')) / window_size
        if at_content > threshold:  # Changed from >= to >
            at_count += 1
        if gc_content > threshold:  # Changed from >= to >
            gc_count += 1
    return {"at_rich_regions": at_count, "gc_rich_regions": gc_count}

def extract_features(sequence: str) -> Dict[str, float]:
    """
    Extract all features from a DNA sequence.
    """
    features = {}
    features.update(extract_basic_info(sequence))
    features.update(count_base_consecutive(sequence, 6, 21))
    features.update(count_pattern_occurrences(sequence, 2, 8))
    features.update(count_pattern_occurrences(sequence, 3, 5))
    features.update(count_pattern_occurrences(sequence, 4, 4))
    features.update(count_rich_regions(sequence, 100, 0.8))
    return features

# Add more feature extraction functions as needed