# Bayesian Changepoint Detection for Single Molecule Analysis

## Introduction
This repository contains Python code for detecting changepoints in single molecule datasets using Bayesian methods. The code allows for both piecewise and stepwise changepoint detection, which can be useful in various scientific analyses where abrupt changes in data need to be identified.

## Repository Structure
```
- main_piecewise_CPdetection.py: Main script for piecewise changepoint detection.
- main_stepwise_CPdetection.py: Main script for stepwise changepoint detection.
- Test_Data/: Directory containing test datasets.
- bayesian_changepoint_detection/: Package with modules for changepoint detection.
- Examples/: Directory with example output data and notebooks.
- Docs/: Documentation related images.
- setup.py: Setup script for installing the package.

```
## Installation and Requirements
To use this code, you will need Python 3.x and the following packages:
- numpy
- matplotlib
- scipy

You can install the required packages using `pip`:
```
pip install numpy matplotlib scipy
```

## Usage
To run the changepoint detection scripts, navigate to the directory containing the scripts and execute them with Python. For example:
```
python main_piecewise_CPdetection.py
python main_stepwise_CPdetection.py
```

## Experimental Data
The `Test_Data/` directory contains experimental datasets that can be used to test the changepoint detection algorithms. The data is typically structured as comma-separated values with columns representing different variables such as time or intensity.

## Contributing
Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact Information
For any queries or assistance, please contact the repository maintainer at [email address].
