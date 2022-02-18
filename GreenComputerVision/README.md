# Motivation
With the current trend in Machine Learning being to 'buy' better results by using a bigger model or more training parameters, this investigation aims to show that there is a disproportionate level of energy waste generated for the marginal improvements seen in task performance.  Training deep learning models consumes a staggering amount of electricity, and as deep learning becomes more prominent, the carbon footprint caused by keeping up with its energy demand is not sustainable.  

<br>

> ### *Are more expensive models worth it?* 

<br>

# Methods and Hardware
* All models are PyTorch implementations and pretrained on ImageNet.
* Models are fine tuned on the MedMNIST pediatric pneumonia dataset.
* Recorded accuracy and AUC as model evaluation metrics.
* GPU - 1 x NVIDIA Tesla T4 (Standard_NC8as_T4_v3 (8 cores, 56 GB RAM, 352 GB disk))
* GPU performance logging completed using Azure Monitor



<br>

# Results


<br>

![EnergyConsumption](https://user-images.githubusercontent.com/80305894/152247072-ee8a1aa1-9fea-4e1e-840b-16d7e7993e2c.png)

<sup><i>The plot above shows the energy consumed by the NVIDIA T4 GPU during fine tuning of each model on the MedMNIST dataset.</i></sup>
<br>
<br>



### Performance Metrics
| **Model** | **ACC** | **AUC** | **Mean GPU Util (%)** | **Runntime (mm:ss)** | **Energy (kJ)** |
| :-------------: | :----------: |  :----------: |  :----------: |  :----------: |  :----------: | 
| DenseNet-121  | 0.851 | 0.972 | 93.6 | 19:59 | 82.3 |
| DenseNet-169  |  0.821 | 0.970 | 95.7 | 25:28 | 104.9 |
| DenseNet-201  |  0.872 | 0.976 | 94.8 | 33:25 | 137.7 |
| ResNet-18  |  0.846 | 0.967 | 82.1 | 04:57 | 20.4 |
| ResNet-50  |  0.837 | 0.942 | 97.6 | 20:33 | 84.7 |
| Inception-v3  |  0.873 | 0.945 | 92.3 | 09:06 | 37.5 |

<br>

# Discussion

### GPU Utilization
All models have relatively the same GPU utilization during fine-tuning.  ResNet-18 had a lower *mean* GPU utilization due to the combination of short runtime and the time granularity of observations. GPU utilization was recorded as a mean over 1 minute intervals, and ResNet-18 ran for just under 5 minutes. These are unweighted means and ResNet-18 has 1 point of low utilization which heavily effected the mean.  The behavior of GPU utilization for ResNet-18 during finetuning had a similar pattern to the other models. Overall, each model used a consistent proportion of the GPU's memory over the duration of the runtime. 

With the consistency in GPU utilization across models, a flat rate for this GPU SKU's energy consumption was 4120 Joules per minute. To put this into terms of the environment, the CO<sub>2</sub> emitted to supply that electricity is the same amount of CO<sub>2</sub> as burning half a kg of coal per minute.


### Impact of Model Size
DenseNet, ResNet

### InceptionV3

*“Based on the exploration of ways to scale up networks in ways that aim at utilizing the added computation as efficiently as possible by suitably factorized convolutions and aggressive regularization.”* 

The Inception-v3 architecture had superior efficiency compared to the tested ResNet and DenseNet implementations. The ACC and AUC were on par with the biggest model tested (DenseNet-201) but finshed fine tuning the ImageNet weights for MedMNIST images in 27% of the time.  Being of a similar depth to ResNet-50, Inception-v3 was able to complete the fine tuning in 44% of the time.  

<br>

> ### *The elephant in the room is that all ACC and AUC are comparable, but runtimes are not!*

<br>

More parameters and more network layers do not directly translate to better model performance. However, CO2 emitted due to the electricity consumed is directly proportional to runtime. Comparing the maximum accuracy improvement seen by increasing the depth of the model (DenseNet-169 vs DenseNet-201), the 5% accuracy gain by increasing the number of layers also meant an extra 4 kg of CO2 were emitted.
Looking the two most accurate models (DenseNet-201 and Inception-v3), training DenseNet on this GPU put another 12 kg of CO2 into the atmosphere and had almost no model performance gain. Things to remember about these runs are that these are ***only fine tuning runs*** and ***the T4 is a relatively small GPU***. With full training of deep learning models easily accruing days’ worth of GPU hours on more powerful hardware the total cost of increased complexity adds up.

The efficiency of the model’s computational architecture is a key sustainability metric. Efficient models reduce total runtime needed as thus lower both environmental costs and operational expense. Researchers need step away from only benchmarking models with performance such metrics such as ACC and AUC, and supplement with a metric such as FLOPS. With many commercial scale deep learning models (such as the models tested) all able to get strong task results, costs become metrics of model selection.
    

<br>


# Resources
| **PyTorch Framework**  |
| :---------- |
| [DenseNet](https://pytorch.org/hub/pytorch_vision_densenet/)  | 
| [ResNet](https://pytorch.org/hub/pytorch_vision_resnet/)| 
| [Inception-v3](https://pytorch.org/hub/pytorch_vision_inception_v3/)|

<br>

| **Archive**  | 
| :---------- |
| [Green AI](https://arxiv.org/abs/1907.10597) |
| [MedMNIST](https://github.com/MedMNIST/MedMNIST)  | 
| [Densely Connected Convolutional Networks](https://arxiv.org/abs/1608.06993) |
| [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385) |
| [Rethinking the Inception Architecture for Computer Vision](https://pytorch.org/hub/pytorch_vision_inception_v3/)| 
| [EPA Equivalencies Calculator](https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator) |

<br>
