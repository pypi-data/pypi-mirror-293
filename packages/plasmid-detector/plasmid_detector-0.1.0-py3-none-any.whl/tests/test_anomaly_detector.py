import pytest
import pandas as pd
import numpy as np
from plasmid_detector.anomaly_detector import AnomalyDetector

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'feature1': np.random.rand(100),
        'feature2': np.random.rand(100),
        'feature3': np.random.rand(100),
    })

def test_anomaly_detector_fit(sample_data):
    detector = AnomalyDetector(n_clusters=3)
    detector.fit(sample_data)
    assert detector.kmeans is not None
    assert detector.centers is not None
    assert detector.covs is not None

def test_anomaly_detector_predict(sample_data):
    detector = AnomalyDetector(n_clusters=3)
    detector.fit(sample_data)
    
    test_data = pd.DataFrame({
        'feature1': np.random.rand(10),
        'feature2': np.random.rand(10),
        'feature3': np.random.rand(10),
    })
    
    anomalies, scores, contributions = detector.predict(test_data, threshold=2.0)
    
    print("Anomalies:", anomalies)
    print("Scores:", scores)
    print("Contributions type:", [type(c) for c in contributions])
    print("Contributions shape:", [c.shape for c in contributions])
    
    assert all(isinstance(a, bool) for a in anomalies)
    assert len(anomalies) == 10
    assert len(scores) == 10
    assert len(contributions) == 10
    assert all(isinstance(s, float) for s in scores)
    assert all(isinstance(c, np.ndarray) for c in contributions)
    assert all(c.shape == (3,) for c in contributions)  # Assuming 3 features

# Add more tests as needed