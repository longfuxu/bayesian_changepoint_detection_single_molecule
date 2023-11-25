from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

from bayesian_changepoint_detection.stepwise_change_functions import *

from bayesian_changepoint_detection.priors import const_prior
from functools import partial

from bayesian_changepoint_detection.bayesian_models import offline_changepoint_detection
import bayesian_changepoint_detection.offline_likelihoods as offline_ll

from bayesian_changepoint_detection.x_index_averager import average_indices


file_path = 'Test_Data/testdata_simulatedDiscreteSteps19.txt'

# file_path = 'Test_Data/testdata_regular_steps.txt'
try:
    # Load the data from the file
    x, data = np.loadtxt(file_path, delimiter=',',unpack=True)

    # Plotting the data
    plt.plot(x, data)
    plt.xlabel('X Label')
    plt.ylabel('Y Label')
    plt.title('Plot Title')
    plt.show()

except IOError:
    print(f"Error: File {file_path} not found.")
except ValueError as e:
    print(f"Error: Could not parse the file {file_path}.")
    print("Details:", e)

# Let's start to analyze the trace
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
closeness_threshold = 10

averaged_indices = average_indices(prob_threshold, closeness_threshold, Pcp)

# Recalculate step sizes based on the optimal step locations
recalculated_step_sizes = recalculate_step_sizes(data[:], averaged_indices)

# Reconstruct and plot the fitted curve
fitted_curve = reconstruct_fitted_curve(x, data, averaged_indices, recalculated_step_sizes)

# Plot the origianl data
plt.figure(figsize=(10,8))
plt.plot(x, data, label="Original Data")
plt.plot(x, fitted_curve, label="Fitted Steps")
plt.xlabel('X-label')
plt.ylabel('Simulated Data')
plt.legend()
plt.show()