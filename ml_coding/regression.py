import numpy as np


class BaseRegression:
    def __init__(self, lr=0.01, epochs=10):
        self.lr = lr
        self.epochs = epochs
        self.w = None
        self.b = None

    def fit(self, X, y):
        n_samples, n_feautres = X.shape

        self.w = np.zeros(n_feautres)
        self.b = 0.0

        for _ in range(self.epochs):
            y_pred = self._approximation(X, self.w, self.b)

            self.dw = (1/n_samples) * np.dot(X.T, (y_pred - y))
            self.db = (1/n_samples) * np.sum(y_pred - y)

            self.w -= self.lr * self.dw
            self.b -= self.lr * self.db

    def predict(self, X):
        return self._predict(X)    
    
    def _approximation(self, X, w, b):
        raise NotImplementedError
    
    def _predict(self, X):
        raise NotImplementedError
    
class LinearRegression(BaseRegression):
    def _approximation(self, X, w, b):
        return np.dot(X, w) + b
    
    def _predict(self, X):
        return np.dot(X, self.w) + self.b
    
class LogisticRegression(BaseRegression):
    def _approximation(self, X, w, b):
        return self._sigmoid(np.dot(X, w) + b)

    def _predict(self, X):
        return self._sigmoid(np.dot(X, self.w) + self.b)
    
    def _sigmoid(self, x):
        """
        1 / (1 + exp(-x))
        """
        return 1 / (np.exp(-x) +1)
    

if __name__ == "__main__": 
    # Example data for Linear Regression
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([2, 4, 6, 8, 10])

    # Train Linear Regression
    lin_model = LinearRegression(lr=0.01, epochs=1000)
    lin_model.fit(X, y)

    # Predict Linear Regression
    y_pred_lin = lin_model.predict(X)

    print("Linear Regression")
    print("Weight:", lin_model.w)
    print("Bias:", lin_model.b)
    print("Predictions:", y_pred_lin)

    # Example data for Logistic Regression
    X_log = np.array([[0.1], [0.4], [0.6], [0.8], [1.0]])
    y_log = np.array([0, 0, 1, 1, 1])

    # Train Logistic Regression
    log_model = LogisticRegression(lr=0.1, epochs=10000)
    log_model.fit(X_log, y_log)

    # Predict Logistic Regression
    y_pred_log = log_model.predict(X_log)

    print("\nLogistic Regression")
    print("Weight:", log_model.w)
    print("Bias:", log_model.b)
    print("Predictions:", y_pred_log)