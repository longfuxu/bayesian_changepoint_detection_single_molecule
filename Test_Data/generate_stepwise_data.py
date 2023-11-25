from bayesian_changepoint_detection.stepwise_change_functions import *
import numpy as np

# Parameters
n_points = 1000
step_locs = [0.05, 0.1, 0.12, 0.15, 0.2, 0.21, 0.24, 0.3, 0.32, 0.4, 0.41, 0.52, 0.55, 0.6, 0.7, 0.77, 0.8, 0.81, 0.85, 0.9]
step_sizes = [1, 2, 3, 4, -1, -2, -3, -4, 1, 2, 3, 4, -1, -2, -3, -4, 1, 2, 3, 4]
noise_std = 1

# Generate data
x, data = generate_step_data(n_points, step_locs, step_sizes, noise_std)
# Save to text file
output_file = 'Test_Data/testdata_stepwise_output_2.txt'
with open(output_file, 'w') as file:
    for x_val, data_val in zip(x, data):
        file.write(f'{x_val},{data_val}\n')

plt.figure(figsize=(10,8))
plt.xlabel('X-index')
plt.ylabel('Simulated Data')
plt.plot(x,data)
plt.show()