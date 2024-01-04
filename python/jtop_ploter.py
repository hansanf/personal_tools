import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from prettytable import PrettyTable
table = PrettyTable(['name', '均值','90 分位','95 分位','99 分位', '最小值', '最大值'])

# Read the CSV into a pandas dataframe
df = pd.read_csv(r'/Users/fengguoqing/Downloads/log.csv')

# Define the columns to plot
# cols = ['CPU1', 'CPU2', 'CPU3', 'CPU4', 'CPU5', 'CPU6', 'CPU7', 'CPU8']
cols = ['GPU']

# Create a new figure and axis object
fig, ax = plt.subplots()

def percentiles(data):
  # print(f"Mean: {np.mean(data):.2f}", end='\t')
  # print(f"Percent 50: {np.percentile(data, 50):.2f}", end='\t')
  # print(f"Percent 90: {np.percentile(data, 90):.2f}", end='\t')
  # print(f"Percent 99: {np.percentile(data, 99):.2f}", end='\t')
  table.add_row(["GPU Utilization\%",
                 f"{np.mean(data):.2f}", 
                 f"{np.percentile(data,90):.2f}",
                 f"{np.percentile(data,95):.2f}",
                 f"{np.percentile(data,99):.2f}",
                 f"{np.min(data):.2f}",
                 f"{np.max(data):.2f}",
                ])

# Plot the columns as a line chart
for col in cols:
  percentiles(df[col])
  ax.plot(df[col], label=col)

# Set the x-axis label
ax.set_xlabel('Time')

# Set the y-axis label
ax.set_ylabel('Usage')

# Add a title to the plot
ax.set_title('Jtop Status Over Time')

# Add a legend to the plot
ax.legend()

# Show the plot
plt.show()

print("")
print(table)