# Import modules.
import pandas as pd
import matplotlib.pyplot as plt

# Read in data from path.
gpu_util_data = pd.read_csv('GpuUtil.csv')
data = pd.read_csv('PlotData.csv')


##########
# Energy Consumption
##########

# Set figure size for landscape layout.
plt.rcParams["figure.figsize"] = [10, 5]

# Create barplot of model energy consumption.
# Convert J to kJ
plt.bar(data['Model'], data['Aprox Energy (J)']/1000, 
        color=['cyan', 'orange','black', 'red', 'green', 'blue'],
        edgecolor='black')

# Add dashed gridlines to graphic.
plt.grid(visible=True, linestyle = '--')
# Add a title to the plot
plt.title("Fine Tuning Energy Consumption for Deep Learning Models", size=16)
# Setting label and fontsize for x-axis. 
plt.xlabel("Model", size=12)
# Setting label and fontsize for y-axis. 
plt.ylabel("Energy (kJ)", size=12)
plt.show()
