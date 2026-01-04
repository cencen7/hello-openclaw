"""
Problem Statement

You are given:
A 1-channel (grayscale) image represented as a 2D array
An arbitrary 2D kernel

Tasks:
Implement 2D convolution
Optimize the implementation for:
Gaussian kernel
Box filter

Assumptions:
No padding (valid convolution)
Output size is smaller than input
Kernel size is known
"""

def convolve_naive1(image, kernel):
    H, W = image.shape
    kH, kW = kernel.shape

    output = np.zeros((H - kH + 1, W - kW + 1))

    for i in range(H - kH + 1):
        for j in range(W - kW + 1):
            s = 0
            for ki in range(kH):
                for kj in range(kW):
                    s += image[i + ki, j + kj] * kernel[ki, kj]
            output[i, j] = s
    return output

def convolve_numpy1(image, kernel):
    H, W = image.shape
    kH, kW = kernel.shape

    out = np.zeros((H - kH + 1, W - kW + 1))

    for i in range(H - kH + 1):
        for j in range(W - kW + 1):
            patch = image[i: i+kH, j: j+kW]
            out[i, j] = np.sum(patch * kernel)
    return out

def convolve_naive(image, kernel):
    image_height, image_width = image.shape
    kernel_height, kernel_width = kernel.shape

    output = np.zeros((
        image_height - kernel_height + 1,
        image_width - kernel_width + 1
    ))

    for i in range(image_height - kernel_height + 1):
        for j in range(image_width - kernel_width + 1):
            s = 0
            for k in range(kernel_height):
                for l in range(kernel_width):
                    s += image[i + k, j + l] * kernel[
                        kernel_height - k - 1,
                        kernel_width - l - 1
                    ]
            output[i, j] = s
    return output





