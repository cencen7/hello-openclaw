from collections import Counter
import numpy as np

class KNN:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_train = np.asarray(X, dtype=np.float32)
        self.y_train = np.asarray(y)

    def predict(self, X):
        X = np.asarray(X, dtype=np.float32)
        return np.array([self._predict(x) for x in X])
    
    def _euclidean_distance(point1, point2):
        return np.sqrt(np.sum((point1 - point2) ** 2))

    def _predict_one_distance(self, x):
        # squared euclidean distances (avoid sqrt; ranking is same)
        dist2 = np.sum((self.X_train - x) ** 2, axis=1)
        return dist2
    
    def _predict(self, x):
        d2 = self._predict_one_distance(x)
        # O(N) average; Partial selection (Quickselect-style), left k are smallest
        k_idx = np.argpartition(d2, self.k)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_idx]
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]


class KNNSlow:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        y_pred = [self._predict(x) for x in X]
        return np.array(y_pred)
    
    def _euclidean_distance(point1, point2):
        return np.sqrt(np.sum((point1 - point2) ** 2))

    def _predict(self, x):
        # compute distance between x and all examples in the training set
        distances = [self._euclidean_distance(x, x_train) for x_train in self.X_train]
        # sort by distance and return indices of the first k neighbors
        k_indices = np.argsort(distances)[:self.k]
        # extract the labels of the k nearest neighbor
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        # return the most common class label
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]