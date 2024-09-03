import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from scipy.spatial.distance import mahalanobis
from typing import Tuple, List

class AnomalyDetector:
    def __init__(self, n_clusters: int = 7, random_state: int = 0):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.kmeans = None
        self.centers = None
        self.covs = None

    def fit(self, data: pd.DataFrame):
        """
        Fit the anomaly detector to the data.
        """
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.random_state, n_init=10).fit(data)
        self.centers = self.kmeans.cluster_centers_
        
        # Calculate covariance matrices for each cluster
        self.covs = []
        for i in range(self.n_clusters):
            cluster_data = data[self.kmeans.labels_ == i]
            cov = np.cov(cluster_data.T, bias=True)
            cov += np.eye(cov.shape[0]) * 1e-6  # Add regularization
            self.covs.append(cov)

    def calculate_anomaly_score(self, data: pd.Series) -> Tuple[float, np.ndarray]:
        label = self.kmeans.predict(data.to_frame().transpose())[0]
        center = self.centers[label]
        inv_covmat = np.linalg.inv(self.covs[label])
        
        diff = data - center
        mahal_dist = np.sqrt(np.dot(np.dot(diff, inv_covmat), diff))
        contributions = np.dot(inv_covmat, diff) * diff
        
        return float(mahal_dist), contributions.to_numpy()

    def predict(self, data: pd.DataFrame, threshold: float) -> Tuple[List[bool], List[float], List[np.ndarray]]:
        anomalies = []
        scores = []
        contributions = []
        
        for _, row in data.iterrows():
            score, contrib = self.calculate_anomaly_score(row)
            anomalies.append(score > threshold)
            scores.append(score)
            contributions.append(contrib)
        
        return anomalies, scores, contributions

def main():
    # This function will be the entry point for the command-line tool
    pass

if __name__ == "__main__":
    main()