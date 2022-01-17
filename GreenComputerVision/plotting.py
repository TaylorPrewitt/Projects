# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 14:15:21 2022

@author: prewi
"""

# Import modules.
import pandas as pd
import matplotlib.pyplot as plt

# Read in data from path.
gpu_util_data = pd.read_csv('GpuUtilPlotTableCsvSep.csv')
data = pd.read_csv('PlotDataOther.csv')

# Set figure size for landscape layout.
plt.rcParams["figure.figsize"] = [25, 10]

# Create plot layers. One layer per model.
res18_gutil = plt.plot(gpu_util_data['ResNet-18'], 
                       c='red', 
                       lw=5, 
                       label='ResNet-18')

res50_gutil = plt.plot(gpu_util_data['ResNet-50'], 
                       c='green',
                       lw=5, 
                       label='ResNet-50')

inceptionv3_gutil = plt.plot(gpu_util_data['Inception-v3'], 
                             c='blue', 
                             lw=5, 
                             label='Inception-v3')

densenet121_gutil = plt.plot(gpu_util_data['DenseNet-121'],
                             c='cyan', 
                             lw=5, 
                             label='DenseNet-121')

densenet169_gutil = plt.plot(gpu_util_data['DenseNet-169'], 
                             c='orange', 
                             lw=5, 
                             label='DenseNet-169')

densenet201_gutil = plt.plot(gpu_util_data['DenseNet-201'], 
                             c='black', 
                             lw=5, 
                             label='DenseNet-201')

# Add dashed gridlines to graphic.
plt.grid(visible=True, linestyle = '--')
# Add a title to the plot
plt.title("GPU Utilization Over MedMNIST Classification Training", size=22)
# Setting label and fontsize for x-axis. 
plt.xlabel("Runtime (minutes)", size=16)
# Limit the tick mark labels.  Labels every 10th minute along axis. 
plt.xticks(ticks=gpu_util_data.iloc[::10, 7])
# Setting label and fontsize for y-axis. 
plt.ylabel("GPU Utilization (%)", size=16)
# Setting y-axis to show tick marks every 10% util over all data range. 
plt.yticks(ticks=range(0,101,10))
# Adding a readable legend and isolating visually. 
plt.legend(frameon=True, prop={"size":20})
plt.show()




##########
# Accuracy
##########

# Set figure size for landscape layout.
plt.rcParams["figure.figsize"] = [10, 5]

# Create barplot of model accuracy. Color coded to match GpuUtil plot. 
plt.bar(data['Model'], data['Test Accuracy'], 
        color=['cyan', 'orange','black', 'red', 'green', 'blue'],
        edgecolor='black')

# Add dashed gridlines to graphic.
plt.grid(visible=True, linestyle = '--')
# Add a title to the plot
plt.title("Model Accuracy on Test Data", size=16)
# Setting label and fontsize for x-axis. 
plt.xlabel("Model", size=12)
# Setting label and fontsize for y-axis. 
plt.ylabel("Accuracy", size=12)
plt.show()



##########
# AUC
##########

# Set figure size for landscape layout.
plt.rcParams["figure.figsize"] = [10, 5]

# Create barplot of model AUC. Color coded to match GpuUtil plot. 
plt.bar(data['Model'], data['AUC'], 
        color=['cyan', 'orange','black', 'red', 'green', 'blue'],
        edgecolor='black')

# Add dashed gridlines to graphic.
plt.grid(visible=True, linestyle = '--')
# Add a title to the plot
plt.title("Model AUC on Test Data", size=16)
# Setting label and fontsize for x-axis. 
plt.xlabel("Model", size=12)
# Setting label and fontsize for y-axis. 
plt.ylabel("AUC", size=12)
plt.show()



##########
# Energy Consumption
##########

# Set figure size for landscape layout.
plt.rcParams["figure.figsize"] = [10, 5]

# Create barplot of model AUC. Color coded to match GpuUtil plot. 
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
