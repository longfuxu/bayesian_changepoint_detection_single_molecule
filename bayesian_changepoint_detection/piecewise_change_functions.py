# In this modual, we defined custom functions intended for piece-wise datasets.

from scipy.signal import savgol_filter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def gradual_change_trace(x, y, noise_stddev):
    """
    Generates a gradual changing trace with pausing events.
    x: A list of lists, each sublist contains the start and end x-coordinate of the segment.
    y: A list of lists, each sublist contains the start and end y-coordinate of the segment.
    noise_stddev: Standard deviation of the Gaussian noise added to the y values.
    """
    x_values = []
    y_values = []

    for i, (x_start, x_end) in enumerate(x):
        y_start, y_end = y[i]
        num_points = int((x_end - x_start) * 1000)
        segment_x = np.linspace(x_start, x_end, num_points)
        segment_y = np.linspace(y_start, y_end, num_points)
        noise = np.random.normal(0, noise_stddev, num_points)
        x_values.extend(segment_x)
        y_values.extend(segment_y + noise)

    return np.array(x_values), np.array(y_values)

# Estimate the noise level of the datasets using MAD method
def estimate_noise_std(data, scaling_factor=1.4826):
    # Calculate the difference between consecutive data points
    diff_data = np.diff(data)
    
    # Calculate the median absolute deviation (MAD) of the difference data
    mad = np.median(np.abs(diff_data - np.median(diff_data)))
    
    # Estimate the standard deviation using the scaling factor
    estimated_std = mad * scaling_factor
    return estimated_std
    
# using the np.pad function to pad the data before applying the moving window filter. 
# This way, the window size remains the same throughout the filtering process, 
# but we avoid extreme values by padding the data.
def moving_window_filter(y_values, window_size):
    padding_size = window_size // 2
    padded_y_values = np.pad(y_values, (padding_size, padding_size), mode='edge')
    filtered_y_values = np.zeros(len(y_values))

    for i in range(len(y_values)):
        left = i
        right = i + window_size
        filtered_y_values[i] = np.mean(padded_y_values[left:right])

    return filtered_y_values

# Function to calculate the first derivative while handing the edge effect
def first_derivative(x, y, window_size):
    first_derivative_values = np.zeros(len(y))
    
    for i in range(len(y)):
        if i < window_size:
            dy = y[i + window_size] - y[0]
            dx = x[i + window_size] - x[0]
        elif i > len(y) - window_size - 1:
            dy = y[-1] - y[i - window_size]
            dx = x[-1] - x[i - window_size]
        else:
            dy = y[i + window_size] - y[i - window_size]
            dx = x[i + window_size] - x[i - window_size]
        
        first_derivative_values[i] = dy / dx
    
    return first_derivative_values

# Based on simulated data, we determine the optimal window size with a base_window_size and a noise_level_muliplier
def optimal_window_size(estimated_noise_y_value):
    # You can adjust the constants to better suit your specific dataset
    # These constants can be determined experimentally
    base_window_size = 21
    noise_level_multiplier = 171

    window_size = base_window_size + int(noise_level_multiplier * estimated_noise_y_value)
    
    # Ensure the window size is odd
    if window_size % 2 == 0:
        window_size += 1
    
    return window_size


# Function to recalculate step sizes based on the mean y values between adjacent step locations
def recalculate_step_sizes(data, step_locs):
    step_sizes = []
    n_steps = len(step_locs)
    for i in range(n_steps):
        if i == 0:
            left_data = data[:step_locs[i]]
        else:
            left_data = data[step_locs[i-1]:step_locs[i]]
        
        if i == n_steps - 1:
            right_data = data[step_locs[i]:]
        else:
            right_data = data[step_locs[i]:step_locs[i+1]]
        
        step_sizes.append(np.mean(right_data) - np.mean(left_data))
    return step_sizes

# Function to reconstruct the fitted step-like curve
def reconstruct_fitted_steps(x, data, steps, step_sizes):
    fitted_curve = np.zeros_like(data)
    for step, step_size in zip(steps, step_sizes):
        fitted_curve[step:] += step_size
    return fitted_curve

# function to reconstruct the fitted data while properly handle the edge of the data
def reconstruct_fitted_data(x_values, filtered_y_values, step_locs):
    fitted_y_values = np.zeros_like(filtered_y_values)
    sorted_step_locs = sorted(step_locs)
    n_step_locs = len(sorted_step_locs)

    for i in range(n_step_locs + 1):
        if i == 0:
            x_start, y_start = x_values[0], filtered_y_values[0]
            x_end, y_end = x_values[sorted_step_locs[i]], filtered_y_values[sorted_step_locs[i]]
            segment_length = sorted_step_locs[i]
        elif i == n_step_locs:
            x_start, y_start = x_values[sorted_step_locs[i - 1]], filtered_y_values[sorted_step_locs[i - 1]]
            x_end, y_end = x_values[-1], filtered_y_values[-1]
            segment_length = len(filtered_y_values) - sorted_step_locs[i - 1]
        else:
            x_start, y_start = x_values[sorted_step_locs[i - 1]], filtered_y_values[sorted_step_locs[i - 1]]
            x_end, y_end = x_values[sorted_step_locs[i]], filtered_y_values[sorted_step_locs[i]]
            segment_length = sorted_step_locs[i] - sorted_step_locs[i - 1]
        
        segment_y = np.linspace(y_start, y_end, segment_length)
        fitted_y_values[sorted_step_locs[i - 1] if i > 0 else 0:sorted_step_locs[i] if i < n_step_locs else len(filtered_y_values)] = segment_y
            
    return fitted_y_values

# Plot all the results out
def plot_data(x_values, y_values, filtered_y_values, first_derivative_values, fitted_y_values):
    """
    The first subplot shows the original data, filtered data, and the first derivative with a double y-axis.
    The second subplot shows the original data and the fitted data. 
    The fitted data are linear segments with x and y both from the filtered_y_values.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # First plot: original data, filtered data, and first derivative with double y-axis
    ax1.plot(x_values, y_values, label='Original Data')
    ax1.plot(x_values[:len(filtered_y_values)], filtered_y_values, label='Filtered Data')
    ax1.set_ylabel('Y Values')
    ax1.legend(loc='upper left')
    
    ax1b = ax1.twinx()
    ax1b.plot(x_values[:len(first_derivative_values)], first_derivative_values, color='g', label='First Derivative')
    ax1b.set_ylabel('First Derivative')
    ax1b.legend(loc='upper right')

    # Second plot: original data and fitted data
    ax2.plot(x_values, y_values, label='Original Data')
    ax2.plot(x_values[:len(fitted_y_values)], fitted_y_values, label='Fitted Data')
    ax2.set_ylabel('Y Values')
    ax2.legend()


