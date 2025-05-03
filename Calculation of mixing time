# The following code was used in conjuction with the sigmoidal curve fitting script to 
# calculate the mixing time for each simulation. 

import numpy as np
from scipy.optimize import fsolve

# Define the logistic derivative
def logistic_derivative(x, a, b, c):
    return (a * b * np.exp(-b * (x - c))) / (1 + np.exp(-b * (x - c)))**2

# Constants (conducted on an individual basis to observe the reliability 
# and accuracy of the model) 
# see sigmoidal curve model script for the constant definitions
a = 0.43 
b = 0.29 
c = 8.27 

# Define the threshold for the gradient - value at which plateau expected to begin
threshold = 0.0001 

# Function to solve for the x-value where gradient equals the threshold
def gradient_threshold(x):
    return logistic_derivative(x, a, b, c) - threshold

# Use fsolve to find the x-value
plateau_x = fsolve(gradient_threshold, c + 1)[0] 
print(f"The plateau begins at approximately x = {plateau_x:.2f}")
