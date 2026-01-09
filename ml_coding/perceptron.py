import numpy as np

class Perceptron:
    def __init__(self, lr=0.01, epoches=1000):
        self.lr = lr
        self.epoches = epoches
        self.weights = None
        self.bias = None
        self.activation_function = self._unit_step_func

    def fit(self, X, y):
        n_samples, n_features = X.shape

        # initialize weights and bias
        self.weights = np.zeros(n_features)
        self.bias = 0

        y_ = np.array([1 if i > 0 else 0 for i in y])

        for _ in range(self.epoches):
            for idx, x_i in enumerate(X):
                linear_output = np.dot(x_i, self.weights) + self.bias
                y_predicted = self.activation_function(linear_output)

                #perceptron update rule
                update = self.lr * (y_[idx] - y_predicted)

                self.weights += update * x_i
                self.bias += update
            print(f"weights: {self.weights}, bias: {self.bias}")

    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        y_predicted = self.activation_function(linear_output)
        return y_predicted
    
    def _unit_step_func(self, x):
        return np.where(x>=0, 1, 0)
    

if __name__ == "__main__":
    # Example usage
    from sklearn.model_selection import train_test_split
    from sklearn import datasets
    from sklearn.metrics import accuracy_score

    # Load dataset
    iris = datasets.load_iris()
    X = iris.data[:100, :2]  # we only take the first 100 samples and first two features
    y = iris.target[:100]

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the perceptron
    p = Perceptron(lr=0.001, epoches=10)
    p.fit(X_train, y_train)

    # Make predictions
    predictions = p.predict(X_test)

    # Evaluate the model
    print("Accuracy:", accuracy_score(y_test, predictions))