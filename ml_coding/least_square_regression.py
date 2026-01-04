import numpy as np

def linear_regression_train(X, y, lr=0.01, epochs=10):
    """
    Train linear regression using gradient descent.

    Args:
        X (np.ndarray): shape (n_samples, n_features)
        y (np.ndarray): shape (n_samples,)
        lr (float): learning rate
        epochs (int): number of iterations

    Returns:
        w (np.ndarray): weights
        b (float): bias
    """

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
