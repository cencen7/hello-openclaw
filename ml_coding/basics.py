import torch
import numpy as np


def relu(x):
    return torch.maximum(x, torch.tensor(0.0))

def sigmoid(x):
    return 1 / (1 + torch.exp(-x))

def tanh(x):
    return (torch.exp(x) - torch.exp(-x)) / (torch.exp(x) + torch.exp(-x))

def softmax(x):
    return torch.exp(x) / torch.sum(torch.exp(x), dim=-1, keepdim=True)

def cross_entropy(y_true, y_pred):
    eps = 1e-12
    y_pred = np.clip(y_pred, eps, 1 - eps) # avoid log(0) issues
    loss = -np.sum(y_true * np.log(y_pred), axis=-1)
    return loss

if __name__ == "__main__":
    x = torch.tensor([1.0, -1.0, 3.0])
    print(relu(x))
    print(sigmoid(x))
    print(tanh(x))
    print(softmax(x))

