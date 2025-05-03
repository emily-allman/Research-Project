# The following code was used to determine the best fit for each mixing curve. 
# This was done on an individual basis to analyse the applicability for each fitting
# Code requires the output csv file at a given fill height from the Lacey mixing code

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Initialise arrays for x and y
x = []
y = []

# Open the CSV file (csv files are an output of Lacey mixing code)
with open('lacey_results_17401_sl_35700.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            x_value = float(row['time'])
            y_value = float(row['sliding_0.10 z lacey'])
            if x_value > 2:  # Filter: Only include x values greater than 2
                x.append(x_value)
                y.append(round(y_value, 3))  # Round y values to 3 decimal places
        except ValueError:
            print(f"Error converting values: {row['time']} or {row['sliding_0.10 z lacey']} are not valid floats")
            continue

# Convert to numpy arrays
x = np.array(x)
y = np.array(y)

# Define a logistic model with a plateau (sigmoidal curve fitting)
def logistic_model(x, a, b, c):
    """
    Logistic function:
    a: Maximum value
    b: Growth rate
    c: Midpoint
    """
    return a / (1 + np.exp(-b * (x - c)))

# Perform curve fitting
params, covariance = curve_fit(logistic_model, x, y, p0=(1, 0.1, np.mean(x))) 
a, b, c = params

# Generate the fitted curve
x_fit = np.linspace(min(x), max(x), 1000) 
y_fit = logistic_model(x_fit, a, b, c)

# Plot the data points and the logistic fit
plt.scatter(x, y, label='Data Points', color='blue')
plt.plot(x_fit, y_fit, label=f'Logistic Fit (Plateau at y={a:.2f})', color='red')

# Display the logistic equation on the plot
equation_text = f"$y = \\frac{{{a:.2f}}}{{1 + e^{{-{b:.2f}(x - {c:.2f})}}}}$"
print(equation_text)
plt.text(0.6 * max(x), 0.7 * max(y), equation_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

# Add labels, legend, and title
plt.xlabel('Time (s)')
plt.ylabel('Lacey Mixing Index')
plt.title('Logistic Fit Incorporating Plateau')
plt.legend()

# Display the plot
plt.show()
