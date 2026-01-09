import numpy as np

class KMeans:
    def __init__(self, K, max_iters, epsilon=1e-4):
        self.K = K
        self.max_iters = max_iters
        self.clusters = [[] for _ in range(self.K)]
        self.centroids = []
        self.epsilon = epsilon

    def fit(self, X):
        self.X = X
        self.n_samples, self.n_features = X.shape

        # initialize centroids
        random_sample_idxs = np.random.choice(
            self.n_samples, self.K, replace=False)
        
        self.centroids = [self.X[idx] for idx in random_sample_idxs]

        # optimize clusters
        for _ in range(self.max_iters):
            # assigne samples to closest centroids
            self.clusters = self._create_clusters(self.centroids)

            # calculate new centroids
            centroids_old = self.centroids
            self.centroids = self._get_centroids(self.clusters)

            # check if converged
            if self._is_converged(centroids_old, self.centroids):
                break
        
        return self._cluster_labels(self.clusters)
    
    def _closest_centroid(self, sample, centroids):
        distances = [np.linalg.norm(sample - point) for point in centroids]
        closest_idx = np.argmin(distances)
        return closest_idx
    
    def _create_clusters(self, centroids):
        clusters = [[] for _ in range(self.K)]
        for idx, sample in enumerate(self.X):
            centroid_idx = self._closest_centroid(sample, centroids)
            clusters[centroid_idx].append(idx)
        return clusters
    
    def _get_centroids(self, clusters):
        centriods = np.zeros((self.K, self.n_features))
        for cluster_idx, cluster in enumerate(clusters):
            cluster_mean = np.mean(self.X[cluster], axis=0)
            centriods[cluster_idx] = cluster_mean
        return centriods
    
    def _is_converged(self, centroids_old, centroids):
        distances = [
            np.linalg.norm(centroids_old[i] - centroids[i]) for i in range(self.K)
            ]
        if np.sum(distances) < self.epsilon:
            return True
        return False
    
    def _cluster_labels(self, clusters):
        labels = np.empty(self.n_samples)
        for cluster_idx, cluster in enumerate(clusters):
            for sample_idx in cluster:
                labels[sample_idx] = cluster_idx
        return labels
    

if __name__ == "__main__":
    from sklearn.datasets import make_blobs
    import matplotlib.pyplot as plt

    X, y = make_blobs(
        n_samples=300, n_features=2, centers=4,
        cluster_std=0.60, random_state=0
    )

    k = 4
    kmeans = KMeans(K=k, max_iters=150)
    y_pred = kmeans.fit(X)
    print(y_pred)

    plt.scatter(X[:, 0], X[:, 1], c=y_pred, s=30, cmap='viridis')
    plt.scatter(
        np.array(kmeans.centroids)[:, 0],
        np.array(kmeans.centroids)[:, 1],
        c='red', s=200, alpha=0.75
    )
    plt.show()
