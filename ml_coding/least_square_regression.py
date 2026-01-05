import numpy as np


class LinearRegression:
    """
    minmize loss: MSE(y, y_pred) = 1/n * sum((y_pred - y)^2)
    y_pred = Xw + b
    
    1/2m(sum((Xw + b - y)^2))

    
    """
    def __init__(self, lr=0.01, epochs=10):
        self.lr = lr
        self.epochs = epochs
        self.w = None
        self.b = None

    def fit(self, X, y):
        n_samples, n_fratures = X.shape

        # initialize weights and bias
        self.weights = np.zeros(n_fratures) # n_features, 1
        self.bias = 0.0

        # gradient descent
        for _ in range(self.epochs):
            y_predicted = np.dot(X, self.weights) + self.bias
            loss = (y_predicted - y) # n_samples, 1
            dw = (1/n_samples) * (np.dot(X.T, loss))
            db = (1/n_samples) * np.sum(loss)

            # update parameters
            self.weights -= self.lr * dw
            self.bias -= self.lr * db
    
    def predict(self, X):
        y_predicted = np.dot(X, self.weights) + self.bias
        return y_predicted
    

if __name__ == "__main__":
    # Example data
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([2, 4, 6, 8, 10])

    # Train
    model = LinearRegression(lr=0.01, epochs=5000)
    model.fit(X, y)

    # Predict
    y_pred = model.predict(X)

    print("Weight:", model.weights)
    print("Bias:", model.bias)
    print("Predictions:", y_pred)
    

"""
def linear_regression_train(X, y, lr=0.01, epochs=10):
    Train linear regression using gradient descent.

    Args:
        X (np.ndarray): shape (n_samples, n_features)
        y (np.ndarray): shape (n_samples,)
        lr (float): learning rate
        epochs (int): number of iterations

    Returns:
        w (np.ndarray): weights
        b (float): bias

    n_samples, n_features = X.shape

    w = np.zeros(n_features)
    b = 0.0

    for i in range(epochs):
        y_pred = X @ w + b

        # loss
        loss = y_pred - y
        print(f"epoch: {i}; loss: {np.mean(loss)}")

        # gradient
        dw = - (1 / n_samples) * X.T @ loss
        db = - np.mean(loss)
        print(f"db: {db}; dw: {dw}")

        # update
        w += lr * dw
        b += lr * db

        
    return w, b
    

def linear_regression_predict(X, w, b):
    return X @ w + b

# Example data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Train
w, b = linear_regression_train(X, y, lr=0.01, epochs=200)

# Predict
y_pred = linear_regression_predict(X, w, b)

print("Weight:", w)
print("Bias:", b)
print("Predictions:", y_pred)

"""


