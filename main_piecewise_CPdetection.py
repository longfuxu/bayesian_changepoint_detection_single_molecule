from __future__ import division
import os
import numpy as np
import matplotlib.pyplot as plt

from bayesian_changepoint_detection.piecewise_change_functions import *

from bayesian_changepoint_detection.priors import const_prior
from functools import partial

from bayesian_changepoint_detection.bayesian_models import offline_changepoint_detection
import bayesian_changepoint_detection.offline_likelihoods as offline_ll

from bayesian_changepoint_detection.x_index_averager import average_indices


file_path = 'Test_Data/testdata_piecewise_output_1.txt'
try:
    # Load the data from the file
    x_values, y_values = np.loadtxt(file_path, delimiter=',',unpack=True)
    # x, data = np.loadtxt(file_path, unpack=True)

    # Plotting the data
    plt.plot(x_values, y_values)
    plt.xlabel('X Label')
    plt.ylabel('Y Label')
    plt.title('Plot Title')
    plt.show()

except IOError:
    print(f"Error: File {file_path} not found.")
except ValueError as e:
    print(f"Error: Could not parse the file {file_path}.")
    print("Details:", e)
# set the window size and scaling factor to get step-like first-derivative trace
# Calculate the optimal window size based on the estimated noise standard deviation
window_size = optimal_window_size(estimate_noise_std(y_values, scaling_factor=1.3))
filtered_y_values = moving_window_filter(y_values, window_size)
# Calculate the filtered_y_values,first_derivative_values,fitted_y_values and plot the data
first_derivative_values = first_derivative(x_values, y_values, window_size)
# filtered_first_derivative = savgol_filter(first_derivative_values, window_length=5, polyorder=3)

data = first_derivative_values

plt.figure(figsize=(10,8))
plt.xlabel('X-index')
plt.ylabel('First Derivative')
plt.plot(x_values, data)
plt.show()

# Let's start to analyze the trace, in this case the first derivative
prior_function = partial(const_prior, p=1/(len(data) + 1))
Q, P, Pcp = offline_changepoint_detection(data, prior_function ,offline_ll.StudentT(),truncate=-50)

# Create a figure and axis object
fig, ax1 = plt.subplots(figsize=(10, 8))
ax2 = ax1.twinx()

# Plot the data
ax1.plot(data[:], color='blue')
ax2.plot(np.exp(Pcp).sum(0), color='red')

# Set the y-limits for the second axis
ax2.set_ylim(0,0.5)

# Set the x-label and y-label for the first axis
ax1.set_xlabel('X-index')
ax1.set_ylabel('Simulated Data')

# Set the y-label for the second axis
ax2.set_ylabel('Probability')

# Show the plot
plt.show()

# set your threshold here
prob_threshold = 0.1
closeness_threshold = 50

averaged_indices = average_indices(prob_threshold, closeness_threshold, Pcp)

# Recalculate step sizes based on the optimal step locations
recalculated_step_sizes = recalculate_step_sizes(data[:], averaged_indices)

# Calculate the filtered_y_values,first_derivative_values,fitted_y_values and plot the data
filtered_y_values = moving_window_filter(y_values, window_size)
first_derivative_values = first_derivative(x_values, filtered_y_values, window_size)
fitted_y_values = reconstruct_fitted_data(x_values, filtered_y_values, averaged_indices)

plot_data(x_values, y_values, filtered_y_values, first_derivative_values, fitted_y_values)
plt.show()

# calculate the data
cp_locations = np.concatenate([[x_values[0]], x_values[averaged_indices], [x_values[-1]]])
step_sizes = recalculated_step_sizes
plateau_lengths = np.diff(cp_locations)
velocity = step_sizes/plateau_lengths[:-1]

# Saving the extracted information
output_directory = 'Test_Outputdata'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Save step locations, step-sizes, and plateau lengths to files
np.savetxt(os.path.join(output_directory, 'piecewise_cp_locations.txt'), cp_locations)
np.savetxt(os.path.join(output_directory, 'piecewise_step_sizes.txt'), step_sizes, fmt='%.5f')
np.savetxt(os.path.join(output_directory, 'piecewise_plateau_lengths.txt'), plateau_lengths)
np.savetxt(os.path.join(output_directory, 'piecewise_velocity_lengths.txt'), velocity )