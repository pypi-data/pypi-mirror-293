import numpy as np


def monte_carlo_integral(func, n_samples=10_000, x=1, y=1, vectorized_func=False):
    samples_x = np.random.rand(n_samples) * x
    samples_y = np.random.rand(n_samples) * y
    if vectorized_func:
        result = np.mean(func(samples_x, samples_y))
    else:
        result = np.mean([func(x, y) for x, y in zip(samples_x, samples_y)])
    return result
