# In this modual, we defined custom functions intended for stepwise datasets.
from scipy.signal import savgol_filter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate step-like data with Gaussian noise using the provided function
def generate_step_data(n_points, step_locs, step_sizes, noise_std):
    x = np.linspace(0, 1, n_points)
    y = np.zeros(n_points)
    for loc, size in zip(step_locs, step_sizes):
        y += size * (x > loc)
    y += np.random.normal(0, noise_std, n_points)
    return x, y

# Function to recalculate step sizes based on the mean values between adjacent step locations
def recalculate_step_sizes(data, step_locs):
    step_sizes = []
    n_steps = len(step_locs)
    for i in range(n_steps):
        left_index = 0 if i == 0 else step_locs[i-1]
        right_index = step_locs[i]
        left_data = data[left_index:right_index]
        right_data = data[right_index:step_locs[i+1]] if i < n_steps - 1 else data[right_index:]
        
        if left_data.size > 0 and right_data.size > 0:
            step_sizes.append(np.mean(right_data) - np.mean(left_data))
        else:
            # Handle edge cases or raise an error if needed
            step_sizes.append(np.nan)  # Placeholder, replace with appropriate logic
    return step_sizes

# Function to reconstruct the fitted curve
def reconstruct_fitted_curve(x, data, steps, step_sizes):
    fitted_curve = np.zeros_like(data)
    for step, step_size in zip(steps, step_sizes):
        fitted_curve[step:] += step_size
    return fitted_curve
