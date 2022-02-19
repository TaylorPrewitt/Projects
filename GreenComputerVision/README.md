# Motivation
With the current trend in Machine Learning being to 'buy' better results by using a bigger model or more training parameters, this investigation aims to show that there is a disproportionate level of energy waste generated for the marginal improvements seen in task performance.  Training deep learning models consumes a staggering amount of electricity, and as deep learning becomes more prominent, the carbon footprint caused by keeping up with its energy demand is an ever growing factor in climate change.    

<br>

> ### *Are more expensive models worth it?* 

<br>

# Background

<br>

# Methods and Hardware
* All models are PyTorch implementations and pretrained on ImageNet.
    * [DensNet-121, -169, and -201](https://pytorch.org/hub/pytorch_vision_densenet/) 
    * [Resnet-18 and -50 ](https://pytorch.org/hub/pytorch_vision_resnet/)
    * [Inception-v3](https://pytorch.org/hub/pytorch_vision_inception_v3/)
* Models are fine tuned to the [MedMNIST](https://github.com/MedMNIST/MedMNIST) pediatric pneumonia dataset for image classification.
* Accuracy and AUC used as model evaluation metrics.
* GPU - 1 x NVIDIA Tesla T4 (Standard_NC8as_T4_v3 (8 cores, 56 GB RAM, 352 GB disk))
* GPU performance logging completed using [Azure Monitor](https://azure.microsoft.com/en-us/services/monitor/#overview)  


<br>

# Results

<br>

![GpuUtil](https://user-images.githubusercontent.com/80305894/154773458-08828442-957a-4c0a-aef9-a288ea54e4ff.png)

<sup><i>The plot above shows each model's mean GPU Utilization per minute on the NVIDIA T4 GPU while fine tuning ImageNet weights to the MedMNIST dataset.</i></sup>

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

<sup><i>The values in the table above are means over 3 trials per model architecture.</i></sup>

<br>

# Discussion

### GPU Utilization
All models had relatively the same GPU utilization during fine-tuning.  ResNet-18 had a lower reported *mean* GPU utilization due to the combination of a short runtime and the time granularity for observations. GPU utilization data was recorded as a mean over 1 minute intervals, and ResNet-18 ran for just under 5 minutes. The *Mean GPU Util (%)* values in the table are unweighted means, and ResNet-18 had 1 point of low utilization (~50%) which heavily effected the mean (Inception-v3 saw this to some degree as well). Overall, the behavior of GPU utilization for ResNet-18 during finetuning had a similar pattern to the other models; the other models had points GPU utilization records near this value as well. In general, each model used a consistent and similar proportion of the GPU's memory over the duration of their runtime.

With the consistency in GPU utilization across models, a flat rate approximation for this GPU SKU's energy consumption was 4120 Joules per minute. To put this into terms of the environment, the CO<sub>2</sub> emitted to supply that electricity is the same amount of CO<sub>2</sub> as burning half a kg of coal per minute ([EPA Equivalencies Calculator](https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator)).

<br>

### Impact of Model Size
#### *DenseNet*
The DenseNet models tested increased in network depth from 121-layers to 201-layers and the number of model parameters scaled similarly as well.  It was expected that the increased depth and parameter count would in turn increase the ACC and AUC scores while also increasing runtime. The models did increase in runtime as the network depth increased, but the ACC and AUC did not behave as expected.  While the 201-layer model did perform as expected by improving ACC and AUC compared to the other DenseNet models, the 169-layer model scored lower in these than the 121-layer model. 

* Maximum difference in ACC amongst DenseNet models was approximately 5%.
* Maximum difference in AUC amongst DenseNet models was 0.6%. 
* Runtime scaled with layers, and the maximum difference amongst DenseNet models was approximately 13.5 minutes.


#### *ResNet*
The ResNet models tested were 18- and 50-layers and like DenseNet increased in parameters as the number of layers increased.  This caused similar result expectations as with DenseNet.  Similar to the DenseNet trials, the ResNet fit expectation with runtime changes, but not with ACC and AUC. ResNet-50 saw a substantial increase in runtime over ResNet-18 but had slightly lower ACC and AUC.  Once again this 

* Maximum difference in ACC amongst ResNet models was approximately 1%.
* Maximum difference in AUC amongst ResNet models was 2.5%. 
* Runtime scaled with layers, and the maximum difference amongst ResNet models was approximately 15.5 minutes 

Comparing two similar jumps in model sizes, DenseNet-169 vs DenseNet-201 and ResNet-18 vs ResNet-50 (each an increase of 32 layers), architecture efficiency was shown.  Built as an improvement to ResNet by having a more efficient architecture for transferring information between layers, the runtime of DenseNet for the 32-layer increase changed by roughly 8 minutes compared to ResNet's 15.5 minute increase.  ACC and AUC remained relatively constant with the changes in network depth and model efficiency. 

<br>

### Inception-v3

*“Based on the exploration of ways to scale up networks in ways that aim at utilizing the added computation as efficiently as possible by suitably factorized convolutions and aggressive regularization.”* ([Rethinking the Inception Architecture for Computer Vision](https://pytorch.org/hub/pytorch_vision_inception_v3/)) 

The Inception-v3 architecture has superior efficiency compared to the tested ResNet and DenseNet implementations. The ACC and AUC were on par with the biggest model tested (DenseNet-201) but finished fine tuning the ImageNet weights for MedMNIST images in 27% of the time.  Being of a similar depth to ResNet-50, Inception-v3 (48-layers) was able to complete the fine tuning in 44% of the time with slightly better (albeit comparable) ACC and AUC.  

<br>

> ### *The elephant in the room is that all ACC and AUC are comparable, but runtimes are not!*

<br>

### The Trade-Off 
More parameters and more network layers do not directly translate to better model performance. However, CO<sub>2</sub> emitted due to the electricity consumed is directly proportional to runtime. Comparing the maximum accuracy improvement seen by increasing the depth of the model (DenseNet-169 vs DenseNet-201), the 5% accuracy gain by increasing the number of layers also meant an extra 4 kg of CO<sub>2</sub> were emitted.

<br>

### Cost at Scale
Looking the two most accurate models (DenseNet-201 and Inception-v3), training DenseNet on this GPU put another 12 kg of CO<sub>2</sub> into the atmosphere and had almost no model performance gain. Things to remember about these runs are that these are ***only fine tuning runs*** and ***the T4 is a relatively small GPU***.  With full training of deep learning models easily accruing days’ worth of GPU hours on more powerful hardware, the total costs of increased complexity add up.  

<br>

### Save the Earth By Saving Money
Echoing the findings from *[Green AI](https://arxiv.org/abs/1907.10597)*, efficiency of a model’s computational architecture is a key sustainability metric. However, sustainability is not the only outcome of using efficiency as a metric, but lowered operational costs are as well. Efficient models **reduce total runtime** and thus lower both environmental costs and operational expenses.  Less runtime equals less energy consumed, and cloud hardware options are traditionally priced per hour (ex: [Azure Pricing](https://azure.microsoft.com/en-us/pricing/details/machine-learning/)). Commercial scale deep learning models (such as the models tested) are all able to get comparable task results which implementation costs become prominent metrics of model selection


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
