import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV into a pandas dataframe
df = pd.read_csv(r'C:\Users\fgq\Documents\fgq_personal\log.csv')

# Define the columns to plot
cpu_cols = ['CPU1', 'CPU2', 'CPU3', 'CPU4', 'CPU5', 'CPU6', 'CPU7', 'CPU8']
gpu_col = 'GPU'

# Create a new figure and axis object
fig, ax = plt.subplots()

# Plot the CPU columns as a line chart
for col in cpu_cols:
    ax.plot(df[col], label=col)

# Plot the GPU column as a line chart
ax.plot(df[gpu_col], label=gpu_col)

# Set the x-axis label
ax.set_xlabel('Time')

# Set the y-axis label
ax.set_ylabel('Usage')

# Add a title to the plot
ax.set_title('CPU and GPU Usage Over Time')

# Add a legend to the plot
ax.legend()

# Show the plot
plt.show()