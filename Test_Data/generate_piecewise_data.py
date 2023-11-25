from bayesian_changepoint_detection.piecewise_change_functions import *
import numpy as np

# Example of the simulated data
x = [[0, 0.1], [0.1, 0.3], [0.3, 0.5], [0.5, 0.7], [0.7, 0.9], [0.9, 1]]
y = [[0, 0.5], [0.5, 0.5], [0.5, 1.5], [1.5, 1.5], [1.5, 1], [1, 1]]

# You can tune the noise level to better simulate your real data
noise_stddev = 0.1

x, data = gradual_change_trace(x, y, noise_stddev)

# Save to text file
output_file = 'Test_Data/testdata_piecewise_output_2.txt'
with open(output_file, 'w') as file:
    for x_val, data_val in zip(x, data):
        file.write(f'{x_val},{data_val}\n')

plt.figure(figsize=(10,8))
plt.xlabel('X-index')
plt.ylabel('Simulated Data')
plt.plot(x,data)
plt.show()